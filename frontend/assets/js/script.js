// Global variables
let currentUser = 1; // Default user ID
let currentFlashcardIndex = 0;
let flashcardSession = [];
let quizData = null;
let currentQuizQuestion = 0;
let quizAnswers = [];
let currentPath = null;

// Tab switching
function switchTab(tabName) {
    document.querySelectorAll('.content').forEach(content => {
        content.classList.remove('active');
    });
    
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    
    // Load data for specific tabs
    if (tabName === 'flashcards') {
        loadFlashcardStats();
    } else if (tabName === 'profile') {
        loadProfileData();
    } else if (tabName === 'paths') {
        loadPathsProgress();
    }
}

// ============================================
// TRANSLATION FUNCTIONS
// ============================================

function swapLanguages() {
    const sourceLang = document.getElementById('sourceLang');
    const targetLang = document.getElementById('targetLang');
    const sourceText = document.getElementById('sourceText');
    const translatedText = document.getElementById('translatedText');
    
    const temp = sourceLang.value;
    sourceLang.value = targetLang.value;
    targetLang.value = temp;
    
    const tempText = sourceText.value;
    sourceText.value = translatedText.textContent !== 'Translation will appear here...' 
        ? translatedText.textContent 
        : '';
    
    if (translatedText.textContent !== 'Translation will appear here...') {
        translatedText.innerHTML = `<p>${tempText}</p>`;
    }
}

async function translateText() {
    const sourceText = document.getElementById('sourceText').value;
    const sourceLang = document.getElementById('sourceLang').value;
    const targetLang = document.getElementById('targetLang').value;
    const translatedText = document.getElementById('translatedText');
    const errorDiv = document.getElementById('translatorError');
    
    if (!sourceText.trim()) {
        errorDiv.textContent = 'Please enter text to translate';
        errorDiv.style.display = 'block';
        return;
    }
    
    errorDiv.style.display = 'none';
    translatedText.innerHTML = '<p class="placeholder">Translating...</p>';
    
    try {
        const response = await fetch('/api/translation/translate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                text: sourceText,
                source_lang: sourceLang,
                target_lang: targetLang,
                user_id: currentUser
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            translatedText.innerHTML = `<p>${data.translated_text}</p>`;
            document.getElementById('copyBtn').style.display = 'inline-block';
            document.getElementById('speakBtn').style.display = 'inline-block';
        } else {
            throw new Error(data.error || 'Translation failed');
        }
    } catch (error) {
        errorDiv.textContent = 'Translation failed: ' + error.message;
        errorDiv.style.display = 'block';
        translatedText.innerHTML = '<p class="placeholder">Translation failed...</p>';
    }
}

function copyTranslation() {
    const translatedText = document.getElementById('translatedText').textContent;
    navigator.clipboard.writeText(translatedText);
    alert('Translation copied to clipboard!');
}

function speakTranslation() {
    const translatedText = document.getElementById('translatedText').textContent;
    const targetLang = document.getElementById('targetLang').value;
    
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(translatedText);
        utterance.lang = targetLang === 'es' ? 'es-ES' : targetLang;
        speechSynthesis.speak(utterance);
    } else {
        alert('Text-to-speech not supported in your browser');
    }
}

function clearTranslation() {
    document.getElementById('sourceText').value = '';
    document.getElementById('translatedText').innerHTML = '<p class="placeholder">Translation will appear here...</p>';
    document.getElementById('translatorError').style.display = 'none';
    document.getElementById('copyBtn').style.display = 'none';
    document.getElementById('speakBtn').style.display = 'none';
}

// ============================================
// CHATBOT FUNCTIONS
// ============================================

function askQuestion(question) {
    document.getElementById('userMessage').value = question;
    sendMessage();
}

async function sendMessage() {
    const userMessageInput = document.getElementById('userMessage');
    const userMessage = userMessageInput.value.trim();
    
    if (!userMessage) return;
    
    addMessage(userMessage, 'user');
    userMessageInput.value = '';
    
    const typingMsg = addMessage('Thinking...', 'bot');
    
    try {
        const response = await fetch('/api/chat/message', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                message: userMessage,
                session_id: 'user_' + currentUser,
                user_id: currentUser
            })
        });
        
        const data = await response.json();
        typingMsg.remove();
        
        if (data.success) {
            addMessage(data.response, 'bot');
        } else {
            addMessage('Sorry, something went wrong: ' + data.error, 'bot');
        }
    } catch (error) {
        typingMsg.remove();
        addMessage('Sorry, I couldn\'t process your message: ' + error.message, 'bot');
    }
    
    scrollToBottom();
}

function addMessage(text, type) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    bubbleDiv.textContent = text;
    
    messageDiv.appendChild(bubbleDiv);
    chatMessages.appendChild(messageDiv);
    
    return messageDiv;
}

function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// ============================================
// FLASHCARD FUNCTIONS
// ============================================

async function loadFlashcardStats() {
    try {
        const response = await fetch(`/api/flashcard/stats?user_id=${currentUser}`);
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('cardsStudied').textContent = data.stats.cards_studied;
            document.getElementById('cardsMastered').textContent = data.stats.mastered_cards;
            document.getElementById('cardsDue').textContent = data.stats.due_today;
            document.getElementById('accuracy').textContent = data.stats.accuracy + '%';
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function loadFlashcards(category) {
    // Update active category button
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    document.getElementById('flashcardStart').style.display = 'flex';
    document.getElementById('flashcardDisplay').style.display = 'none';
}

async function startFlashcardPractice() {
    const activeCategory = document.querySelector('.category-btn.active').textContent;
    const category = activeCategory === 'All' ? null : activeCategory.toLowerCase();
    
    try {
        const url = `/api/flashcard/practice?user_id=${currentUser}&count=10${category ? '&category=' + category : ''}`;
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success && data.cards.length > 0) {
            flashcardSession = data.cards;
            currentFlashcardIndex = 0;
            document.getElementById('flashcardStart').style.display = 'none';
            document.getElementById('flashcardDisplay').style.display = 'block';
            showFlashcard();
        } else {
            alert('No flashcards available. Try a different category!');
        }
    } catch (error) {
        console.error('Error loading flashcards:', error);
        alert('Failed to load flashcards');
    }
}

function showFlashcard() {
    if (currentFlashcardIndex >= flashcardSession.length) {
        // Session complete
        alert('Practice session complete! Great job! 🎉');
        document.getElementById('flashcardDisplay').style.display = 'none';
        document.getElementById('flashcardStart').style.display = 'flex';
        loadFlashcardStats();
        return;
    }
    
    const card = flashcardSession[currentFlashcardIndex];
    document.getElementById('currentCard').textContent = currentFlashcardIndex + 1;
    document.getElementById('totalCards').textContent = flashcardSession.length;
    document.getElementById('cardFront').textContent = card.spanish_word;
    document.getElementById('cardBack').textContent = card.english_word;
    document.getElementById('cardExample').textContent = card.example_sentence || '';
    
    // Reset flip
    document.getElementById('card').classList.remove('flipped');
}

function flipCard() {
    document.getElementById('card').classList.toggle('flipped');
}

async function reviewCard(correct) {
    const card = flashcardSession[currentFlashcardIndex];
    
    try {
        await fetch('/api/flashcard/review', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                user_id: currentUser,
                flashcard_id: card.id,
                correct: correct
            })
        });
        
        currentFlashcardIndex++;
        showFlashcard();
    } catch (error) {
        console.error('Error recording review:', error);
    }
}

function skipCard() {
    currentFlashcardIndex++;
    showFlashcard();
}

// ============================================
// QUIZ FUNCTIONS
// ============================================

function selectQuizType(type) {
    document.getElementById('quizSelection').style.display = 'none';
    document.getElementById('quizPlaying').style.display = 'block';
    startQuiz(type);
}

async function startQuiz(type) {
    try {
        const response = await fetch('/api/quiz/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                quiz_type: type,
                count: 10,
                category: type === 'vocabulary' ? 'greetings' : null,
                topic: type === 'grammar' ? 'ser_estar' : 'mixed'
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            quizData = data.quiz;
            currentQuizQuestion = 0;
            quizAnswers = [];
            showQuizQuestion();
        }
    } catch (error) {
        console.error('Error starting quiz:', error);
        alert('Failed to start quiz');
    }
}

function showQuizQuestion() {
    const question = quizData.questions[currentQuizQuestion];
    
    document.getElementById('quizCurrentQ').textContent = currentQuizQuestion + 1;
    document.getElementById('quizTotalQ').textContent = quizData.questions.length;
    document.getElementById('quizQuestion').textContent = question.question;
    
    const optionsDiv = document.getElementById('quizOptions');
    optionsDiv.innerHTML = '';
    
    question.options.forEach((option, index) => {
        const btn = document.createElement('button');
        btn.className = 'quiz-option';
        btn.textContent = option;
        btn.onclick = () => selectQuizAnswer(option, btn);
        optionsDiv.appendChild(btn);
    });
    
    document.getElementById('nextBtn').disabled = true;
    
    const progress = ((currentQuizQuestion + 1) / quizData.questions.length) * 100;
    document.getElementById('quizProgressFill').style.width = progress + '%';
}

function selectQuizAnswer(answer, btn) {
    // Remove previous selection
    document.querySelectorAll('.quiz-option').forEach(opt => {
        opt.classList.remove('selected');
    });
    
    btn.classList.add('selected');
    quizAnswers[currentQuizQuestion] = answer;
    document.getElementById('nextBtn').disabled = false;
}

function nextQuestion() {
    if (currentQuizQuestion < quizData.questions.length - 1) {
        currentQuizQuestion++;
        showQuizQuestion();
    } else {
        finishQuiz();
    }
}

async function finishQuiz() {
    try {
        const response = await fetch('/api/quiz/grade', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                user_id: currentUser,
                quiz_type: quizData.quiz_type,
                topic: quizData.topic || 'mixed',
                answers: quizAnswers,
                questions: quizData.questions
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showQuizResults(data.results);
        }
    } catch (error) {
        console.error('Error grading quiz:', error);
        alert('Failed to grade quiz');
    }
}

function showQuizResults(results) {
    document.getElementById('quizPlaying').style.display = 'none';
    document.getElementById('quizResults').style.display = 'block';
    
    document.getElementById('quizScore').textContent = results.score;
    document.getElementById('quizFeedback').textContent = results.feedback;
    document.getElementById('quizCorrect').textContent = results.correct;
    document.getElementById('quizIncorrect').textContent = results.total - results.correct;
    document.getElementById('quizPercentage').textContent = results.percentage + '%';
}

function retakeQuiz() {
    startQuiz(quizData.quiz_type);
    document.getElementById('quizResults').style.display = 'none';
    document.getElementById('quizPlaying').style.display = 'block';
}

function backToQuizSelection() {
    document.getElementById('quizResults').style.display = 'none';
    document.getElementById('quizSelection').style.display = 'block';
}

// ============================================
// LEARNING PATHS FUNCTIONS
// ============================================

async function loadPathsProgress() {
    const paths = ['beginner', 'intermediate', 'advanced'];
    
    for (const path of paths) {
        try {
            const response = await fetch(`/api/path/progress?user_id=${currentUser}&path_name=${path}`);
            const data = await response.json();
            
            if (data.success) {
                const progress = data.progress.progress_percent;
                document.getElementById(`${path}Progress`).style.width = progress + '%';
                document.getElementById(`${path}Percent`).textContent = progress;
            }
        } catch (error) {
            console.error(`Error loading ${path} progress:`, error);
        }
    }
}

async function selectPath(pathName) {
    currentPath = pathName;
    
    try {
        const response = await fetch(`/api/path/details/${pathName}`);
        const data = await response.json();
        
        if (data.success) {
            document.querySelector('.path-cards').style.display = 'none';
            document.getElementById('pathLessons').style.display = 'block';
            document.getElementById('pathTitle').textContent = data.path.name;
            
            const lessonsList = document.getElementById('lessonsList');
            lessonsList.innerHTML = '';
            
            // Get user progress
            const progressResponse = await fetch(`/api/path/progress?user_id=${currentUser}&path_name=${pathName}`);
            const progressData = await progressResponse.json();
            const completedIds = progressData.success ? progressData.progress.completed_lesson_ids : [];
            
            data.path.lessons.forEach((lesson, index) => {
                const lessonDiv = document.createElement('div');
                const isCompleted = completedIds.includes(lesson.id);
                const isNext = !isCompleted && (index === 0 || completedIds.includes(data.path.lessons[index - 1].id));
                
                lessonDiv.className = `lesson-card ${isCompleted ? 'completed' : ''} ${isNext ? 'current' : ''} ${!isCompleted && !isNext ? 'locked' : ''}`;
                lessonDiv.innerHTML = `
                    <div class="lesson-number">${index + 1}</div>
                    <div class="lesson-content">
                        <h4>${isCompleted ? '✓' : isNext ? '→' : '🔒'} ${lesson.title}</h4>
                        <p>${lesson.description}</p>
                        <div class="lesson-meta">
                            <span>⏱️ ${lesson.estimated_hours} hours</span>
                            ${lesson.topics ? `<span>📚 ${lesson.topics.length} topics</span>` : ''}
                        </div>
                        ${isNext && !isCompleted ? `<button onclick="completeLesson('${lesson.id}')" class="btn btn-sm btn-primary">Complete Lesson</button>` : ''}
                    </div>
                `;
                lessonsList.appendChild(lessonDiv);
            });
        }
    } catch (error) {
        console.error('Error loading path:', error);
    }
}

async function completeLesson(lessonId) {
    try {
        const response = await fetch('/api/path/complete', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                user_id: currentUser,
                path_name: currentPath,
                lesson_id: lessonId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Lesson completed! 🎉');
            selectPath(currentPath); // Reload
        }
    } catch (error) {
        console.error('Error completing lesson:', error);
    }
}

function backToPathSelection() {
    document.querySelector('.path-cards').style.display = 'grid';
    document.getElementById('pathLessons').style.display = 'none';
    loadPathsProgress();
}

// ============================================
// PROFILE FUNCTIONS
// ============================================

async function loadProfileData() {
    try {
        // Load gamification summary
        const response = await fetch(`/api/gamification/summary?user_id=${currentUser}`);
        const data = await response.json();
        
        if (data.success) {
            const summary = data.summary;
            document.getElementById('profilePoints').textContent = summary.points;
            document.getElementById('profileLevel').textContent = summary.level;
            document.getElementById('profileStreak').textContent = summary.streak_days;
            document.getElementById('profileBadges').textContent = summary.badges_earned;
            
            // Level progress
            const pointsToNext = summary.points_to_next_level;
            const progress = ((100 - pointsToNext) / 100) * 100;
            document.getElementById('levelFill').style.width = progress + '%';
            document.getElementById('levelText').textContent = `${100 - pointsToNext} / 100 XP to next level`;
        }
        
        // Load badges
        const badgesResponse = await fetch(`/api/gamification/badges?user_id=${currentUser}`);
        const badgesData = await badgesResponse.json();
        
        if (badgesData.success) {
            const badgesGrid = document.getElementById('badgesGrid');
            badgesGrid.innerHTML = '';
            
            badgesData.badges.forEach(badge => {
                const badgeDiv = document.createElement('div');
                badgeDiv.className = `badge-item ${badge.earned ? 'earned' : 'locked'}`;
                badgeDiv.innerHTML = `
                    <div class="badge-icon">${badge.icon}</div>
                    <div class="badge-name">${badge.name}</div>
                    <div class="badge-desc">${badge.description}</div>
                `;
                badgesGrid.appendChild(badgeDiv);
            });
        }
        
        // Load leaderboard
        const leaderboardResponse = await fetch('/api/gamification/leaderboard?limit=10');
        const leaderboardData = await leaderboardResponse.json();
        
        if (leaderboardData.success) {
            const leaderboardList = document.getElementById('leaderboardList');
            leaderboardList.innerHTML = '';
            
            leaderboardData.leaderboard.forEach((user, index) => {
                const userDiv = document.createElement('div');
                userDiv.className = 'leaderboard-item';
                userDiv.innerHTML = `
                    <span class="rank">#${index + 1}</span>
                    <span class="username">${user.username || 'User ' + user.id}</span>
                    <span class="points">${user.points} pts</span>
                    <span class="streak">🔥 ${user.streak_days}</span>
                `;
                leaderboardList.appendChild(userDiv);
            });
        }
        
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Spanish Learning AI Assistant loaded');
    loadProfileData();
});


// ============================================
// VISUAL LEARNING FUNCTIONS (YOLO + Deep SORT)
// ============================================

let webcamStream = null;
let webcamActive = false;
let detectedVocabulary = new Map(); // Track unique vocabulary

async function startWebcam() {
    try {
        // Request webcam access
        webcamStream = await navigator.mediaDevices.getUserMedia({
            video: { width: 640, height: 480 }
        });
        
        const video = document.getElementById('webcam');
        video.srcObject = webcamStream;
        video.style.display = 'block';
        
        document.getElementById('videoPlaceholder').style.display = 'none';
        document.getElementById('detectionResult').style.display = 'none';
        
        webcamActive = true;
        
        // Update button states
        document.getElementById('startWebcamBtn').disabled = true;
        document.getElementById('stopWebcamBtn').disabled = false;
        document.getElementById('captureBtn').disabled = false;
        
        showNotification('Webcam started successfully', 'success');
    } catch (error) {
        showNotification('Failed to access webcam: ' + error.message, 'error');
        console.error('Webcam error:', error);
    }
}

function stopWebcam() {
    if (webcamStream) {
        webcamStream.getTracks().forEach(track => track.stop());
        webcamStream = null;
    }
    
    const video = document.getElementById('webcam');
    video.srcObject = null;
    video.style.display = 'none';
    
    document.getElementById('videoPlaceholder').style.display = 'flex';
    
    webcamActive = false;
    
    // Update button states
    document.getElementById('startWebcamBtn').disabled = false;
    document.getElementById('stopWebcamBtn').disabled = true;
    document.getElementById('captureBtn').disabled = true;
    
    showNotification('Webcam stopped', 'info');
}

async function captureFrame() {
    if (!webcamActive) {
        showNotification('Webcam is not active', 'error');
        return;
    }
    
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('webcamCanvas');
    const ctx = canvas.getContext('2d');
    
    // Set canvas size to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw current frame to canvas
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convert to base64
    const imageData = canvas.toDataURL('image/jpeg');
    
    // Send to detection API
    await detectObjects(imageData);
}

function uploadImage() {
    document.getElementById('imageUpload').click();
}

async function processUploadedImage() {
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput.files[0];
    
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = async function(e) {
        const imageData = e.target.result;
        
        // Hide video, show result image
        document.getElementById('webcam').style.display = 'none';
        document.getElementById('videoPlaceholder').style.display = 'none';
        
        await detectObjects(imageData);
    };
    reader.readAsDataURL(file);
}

async function detectObjects(imageData) {
    try {
        showNotification('Detecting objects...', 'info');
        
        const response = await fetch('/api/visual/detect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                image: imageData,
                confidence: 0.5
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Display result image with bounding boxes
            const resultImg = document.getElementById('detectionResult');
            resultImg.src = data.image;
            resultImg.style.display = 'block';
            
            // Hide webcam video
            if (webcamActive) {
                document.getElementById('webcam').style.display = 'none';
            }
            
            // Update detected objects list
            updateDetectedObjects(data.detections);
            
            // Update stats
            document.getElementById('objectCount').textContent = data.count;
            document.getElementById('uniqueWords').textContent = detectedVocabulary.size;
            
            // Enable save button if objects detected
            if (data.count > 0) {
                document.getElementById('saveFlashcardsBtn').disabled = false;
            }
            
            showNotification(`Detected ${data.count} objects!`, 'success');
        } else {
            throw new Error(data.error || 'Detection failed');
        }
    } catch (error) {
        showNotification('Detection error: ' + error.message, 'error');
        console.error('Detection error:', error);
    }
}

function updateDetectedObjects(detections) {
    const listDiv = document.getElementById('detectedObjectsList');
    
    if (detections.length === 0) {
        listDiv.innerHTML = '<p class="placeholder-text">No objects detected</p>';
        return;
    }
    
    // Add to vocabulary map
    detections.forEach(det => {
        if (!detectedVocabulary.has(det.english)) {
            detectedVocabulary.set(det.english, {
                spanish: det.spanish,
                count: 1
            });
        } else {
            const vocab = detectedVocabulary.get(det.english);
            vocab.count++;
        }
    });
    
    // Build HTML
    let html = '<div class="detected-items">';
    detections.forEach(det => {
        html += `
            <div class="detected-item">
                <div class="detected-label">
                    <span class="track-id">ID: ${det.track_id}</span>
                    <span class="english-word">${det.english}</span>
                    <span class="spanish-word">${det.spanish}</span>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: ${det.confidence * 100}%"></div>
                </div>
                <span class="confidence-text">${(det.confidence * 100).toFixed(0)}%</span>
            </div>
        `;
    });
    html += '</div>';
    
    listDiv.innerHTML = html;
    
    // Update vocabulary grid
    updateVocabularyGrid();
}

function updateVocabularyGrid() {
    const gridDiv = document.getElementById('vocabularyGrid');
    
    if (detectedVocabulary.size === 0) {
        gridDiv.innerHTML = '<p class="placeholder-text">No vocabulary yet</p>';
        return;
    }
    
    let html = '';
    detectedVocabulary.forEach((data, english) => {
        html += `
            <div class="vocab-card">
                <div class="vocab-english">${english}</div>
                <div class="vocab-arrow">→</div>
                <div class="vocab-spanish">${data.spanish}</div>
                <div class="vocab-count">${data.count}×</div>
            </div>
        `;
    });
    
    gridDiv.innerHTML = html;
}

async function saveToFlashcards() {
    try {
        const response = await fetch('/api/visual/vocabulary/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: currentUser })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(`Added ${data.added_count} new flashcards!`, 'success');
            document.getElementById('saveFlashcardsBtn').disabled = true;
        } else {
            throw new Error(data.error || 'Failed to save flashcards');
        }
    } catch (error) {
        showNotification('Error saving flashcards: ' + error.message, 'error');
    }
}

async function clearSession() {
    try {
        const response = await fetch('/api/visual/session/reset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Clear local state
            detectedVocabulary.clear();
            
            // Reset UI
            document.getElementById('objectCount').textContent = '0';
            document.getElementById('uniqueWords').textContent = '0';
            document.getElementById('detectedObjectsList').innerHTML = '<p class="placeholder-text">No objects detected yet</p>';
            document.getElementById('vocabularyGrid').innerHTML = '<p class="placeholder-text">No vocabulary yet</p>';
            document.getElementById('saveFlashcardsBtn').disabled = true;
            
            // Hide result image
            document.getElementById('detectionResult').style.display = 'none';
            
            // Show webcam if active
            if (webcamActive) {
                document.getElementById('webcam').style.display = 'block';
            } else {
                document.getElementById('videoPlaceholder').style.display = 'flex';
            }
            
            showNotification('Session cleared', 'success');
        }
    } catch (error) {
        showNotification('Error clearing session: ' + error.message, 'error');
    }
}

function showNotification(message, type = 'info') {
    // Simple notification system
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#0080ff'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
`;
document.head.appendChild(style);
