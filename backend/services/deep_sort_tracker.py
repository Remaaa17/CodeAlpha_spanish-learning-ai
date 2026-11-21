"""
Deep SORT Object Tracker
Implements Deep SORT algorithm for multi-object tracking
"""

import numpy as np
from scipy.optimize import linear_sum_assignment
from filterpy.kalman import KalmanFilter


class KalmanBoxTracker:
    """
    Represents the internal state of individual tracked objects using Kalman Filter.
    """
    count = 0
    
    def __init__(self, bbox):
        """
        Initialize a tracker using initial bounding box
        bbox: [x1, y1, x2, y2]
        """
        # Define constant velocity model
        self.kf = KalmanFilter(dim_x=7, dim_z=4)
        self.kf.F = np.array([
            [1,0,0,0,1,0,0],
            [0,1,0,0,0,1,0],
            [0,0,1,0,0,0,1],
            [0,0,0,1,0,0,0],
            [0,0,0,0,1,0,0],
            [0,0,0,0,0,1,0],
            [0,0,0,0,0,0,1]
        ])
        
        self.kf.H = np.array([
            [1,0,0,0,0,0,0],
            [0,1,0,0,0,0,0],
            [0,0,1,0,0,0,0],
            [0,0,0,1,0,0,0]
        ])
        
        self.kf.R[2:,2:] *= 10.
        self.kf.P[4:,4:] *= 1000.
        self.kf.P *= 10.
        self.kf.Q[-1,-1] *= 0.01
        self.kf.Q[4:,4:] *= 0.01
        
        self.kf.x[:4] = self._convert_bbox_to_z(bbox)
        self.time_since_update = 0
        self.id = KalmanBoxTracker.count
        KalmanBoxTracker.count += 1
        self.history = []
        self.hits = 0
        self.hit_streak = 0
        self.age = 0
        
    def _convert_bbox_to_z(self, bbox):
        """
        Convert bounding box [x1,y1,x2,y2] to [x,y,s,r]
        where x,y is center, s is scale/area, r is aspect ratio
        """
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = bbox[0] + w/2.
        y = bbox[1] + h/2.
        s = w * h
        r = w / float(h) if h != 0 else 1
        return np.array([x, y, s, r]).reshape((4, 1))
    
    def _convert_x_to_bbox(self, x):
        """
        Convert [x,y,s,r] to bounding box [x1,y1,x2,y2]
        """
        w = np.sqrt(x[2] * x[3])
        h = x[2] / w if w != 0 else 1
        return np.array([
            x[0] - w/2.,
            x[1] - h/2.,
            x[0] + w/2.,
            x[1] + h/2.
        ]).reshape((1, 4))
    
    def update(self, bbox):
        """
        Update the state with new observation
        """
        self.time_since_update = 0
        self.history = []
        self.hits += 1
        self.hit_streak += 1
        self.kf.update(self._convert_bbox_to_z(bbox))
    
    def predict(self):
        """
        Advance state and return predicted bounding box
        """
        if (self.kf.x[6] + self.kf.x[2]) <= 0:
            self.kf.x[6] *= 0.0
        self.kf.predict()
        self.age += 1
        if self.time_since_update > 0:
            self.hit_streak = 0
        self.time_since_update += 1
        self.history.append(self._convert_x_to_bbox(self.kf.x))
        return self.history[-1]
    
    def get_state(self):
        """
        Return current bounding box estimate
        """
        return self._convert_x_to_bbox(self.kf.x)


class DeepSORTTracker:
    """
    Deep SORT Tracker for multi-object tracking
    """
    
    def __init__(self, max_age=30, min_hits=3, iou_threshold=0.3):
        """
        Initialize Deep SORT tracker
        
        Args:
            max_age: Maximum frames to keep track without detection
            min_hits: Minimum hits to consider a track valid
            iou_threshold: IOU threshold for matching
        """
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold
        self.trackers = []
        self.frame_count = 0
    
    def _iou(self, bbox1, bbox2):
        """
        Calculate Intersection over Union (IoU)
        bbox: [x1, y1, x2, y2]
        """
        x1 = max(bbox1[0], bbox2[0])
        y1 = max(bbox1[1], bbox2[1])
        x2 = min(bbox1[2], bbox2[2])
        y2 = min(bbox1[3], bbox2[3])
        
        inter_area = max(0, x2 - x1) * max(0, y2 - y1)
        
        bbox1_area = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1])
        bbox2_area = (bbox2[2] - bbox2[0]) * (bbox2[3] - bbox2[1])
        
        union_area = bbox1_area + bbox2_area - inter_area
        
        if union_area == 0:
            return 0
        
        return inter_area / union_area
    
    def _associate_detections_to_trackers(self, detections, trackers):
        """
        Assign detections to tracked objects using Hungarian algorithm
        
        Returns:
            matches: paired detection-tracker indices
            unmatched_detections: detection indices without match
            unmatched_trackers: tracker indices without match
        """
        if len(trackers) == 0:
            return np.empty((0, 2), dtype=int), np.arange(len(detections)), np.empty((0,), dtype=int)
        
        # Calculate IOU matrix
        iou_matrix = np.zeros((len(detections), len(trackers)), dtype=np.float32)
        for d, det in enumerate(detections):
            for t, trk in enumerate(trackers):
                iou_matrix[d, t] = self._iou(det, trk)
        
        # Hungarian algorithm for matching
        if min(iou_matrix.shape) > 0:
            a = (iou_matrix > self.iou_threshold).astype(np.int32)
            if a.sum(1).max() == 1 and a.sum(0).max() == 1:
                matched_indices = np.stack(np.where(a), axis=1)
            else:
                row_ind, col_ind = linear_sum_assignment(-iou_matrix)
                matched_indices = np.stack([row_ind, col_ind], axis=1)
        else:
            matched_indices = np.empty((0, 2), dtype=int)
        
        unmatched_detections = []
        for d, det in enumerate(detections):
            if d not in matched_indices[:, 0]:
                unmatched_detections.append(d)
        
        unmatched_trackers = []
        for t, trk in enumerate(trackers):
            if t not in matched_indices[:, 1]:
                unmatched_trackers.append(t)
        
        # Filter out matched with low IOU
        matches = []
        for m in matched_indices:
            if iou_matrix[m[0], m[1]] < self.iou_threshold:
                unmatched_detections.append(m[0])
                unmatched_trackers.append(m[1])
            else:
                matches.append(m.reshape(1, 2))
        
        if len(matches) == 0:
            matches = np.empty((0, 2), dtype=int)
        else:
            matches = np.concatenate(matches, axis=0)
        
        return matches, np.array(unmatched_detections), np.array(unmatched_trackers)
    
    def update(self, detections):
        """
        Update tracker with new detections
        
        Args:
            detections: list of detections [[x1,y1,x2,y2], ...]
        
        Returns:
            tracked_objects: list of [x1,y1,x2,y2,track_id]
        """
        self.frame_count += 1
        
        # Get predicted locations from existing trackers
        trks = np.zeros((len(self.trackers), 5))
        to_del = []
        ret = []
        
        for t, trk in enumerate(trks):
            pos = self.trackers[t].predict()[0]
            trk[:] = [pos[0], pos[1], pos[2], pos[3], 0]
            if np.any(np.isnan(pos)):
                to_del.append(t)
        
        trks = np.ma.compress_rows(np.ma.masked_invalid(trks))
        for t in reversed(to_del):
            self.trackers.pop(t)
        
        # Match detections to trackers
        matched, unmatched_dets, unmatched_trks = self._associate_detections_to_trackers(
            detections, trks[:, :4]
        )
        
        # Update matched trackers
        for m in matched:
            self.trackers[m[1]].update(detections[m[0]])
        
        # Create new trackers for unmatched detections
        for i in unmatched_dets:
            trk = KalmanBoxTracker(detections[i])
            self.trackers.append(trk)
        
        # Return tracked objects
        i = len(self.trackers)
        for trk in reversed(self.trackers):
            d = trk.get_state()[0]
            if (trk.time_since_update < 1) and (trk.hit_streak >= self.min_hits or self.frame_count <= self.min_hits):
                ret.append(np.concatenate((d, [trk.id + 1])).reshape(1, -1))
            i -= 1
            
            # Remove dead tracklets
            if trk.time_since_update > self.max_age:
                self.trackers.pop(i)
        
        if len(ret) > 0:
            return np.concatenate(ret)
        return np.empty((0, 5))
    
    def reset(self):
        """Reset tracker"""
        self.trackers = []
        self.frame_count = 0
        KalmanBoxTracker.count = 0
