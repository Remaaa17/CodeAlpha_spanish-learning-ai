# Spanish Learning AI - Complete Feature Test Script
# Tests all 6 features to verify functionality

Write-Host ""
Write-Host "SPANISH LEARNING AI - FEATURE TEST SUITE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:5000"

# Test 1: Translation
Write-Host "Test 1: Translation API" -ForegroundColor Yellow
$body = @{
    text = "Hello, how are you?"
    source_lang = "en"
    target_lang = "es"
    user_id = 1
} | ConvertTo-Json
try {
    $result = Invoke-RestMethod -Uri "$baseUrl/api/translation/translate" -Method POST -ContentType "application/json" -Body $body
    if ($result.success) {
        Write-Host "PASS: Translation works!" -ForegroundColor Green
        Write-Host "   English: Hello, how are you?" -ForegroundColor Gray
        Write-Host "   Spanish: $($result.translated_text)" -ForegroundColor Gray
    }
} catch {
    Write-Host "FAIL: Translation error" -ForegroundColor Red
}
Write-Host ""

# Test 2: Chatbot
Write-Host "Test 2: Chatbot API" -ForegroundColor Yellow
$body = @{
    message = "How do I say hello?"
    user_id = 1
} | ConvertTo-Json
try {
    $result = Invoke-RestMethod -Uri "$baseUrl/api/chat/message" -Method POST -ContentType "application/json" -Body $body
    if ($result.response) {
        Write-Host "PASS: Chatbot responding!" -ForegroundColor Green
        $preview = if ($result.response.Length -gt 50) { $result.response.Substring(0, 50) + "..." } else { $result.response }
        Write-Host "   Response: $preview" -ForegroundColor Gray
    }
} catch {
    Write-Host "FAIL: Chatbot error" -ForegroundColor Red
}
Write-Host ""

# Test 3: Flashcards
Write-Host "Test 3: Flashcard System" -ForegroundColor Yellow
try {
    $result = Invoke-RestMethod -Uri "$baseUrl/api/flashcard/practice?user_id=1&count=3"
    if ($result.success -and $result.cards.Count -gt 0) {
        Write-Host "PASS: Flashcards loading!" -ForegroundColor Green
        Write-Host "   Loaded $($result.cards.Count) cards:" -ForegroundColor Gray
        foreach ($card in $result.cards) {
            Write-Host "   - $($card.spanish_word) = $($card.english_word) [$($card.category)]" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "FAIL: Flashcard error" -ForegroundColor Red
}
Write-Host ""

# Test 4: Quiz Generation
Write-Host "Test 4: Quiz System" -ForegroundColor Yellow
$body = @{
    quiz_type = "vocabulary"
    count = 3
} | ConvertTo-Json
try {
    $result = Invoke-RestMethod -Uri "$baseUrl/api/quiz/generate" -Method POST -ContentType "application/json" -Body $body
    if ($result.success -and $result.quiz.questions.Count -gt 0) {
        Write-Host "PASS: Quiz generation works!" -ForegroundColor Green
        Write-Host "   Generated $($result.quiz.questions.Count) questions:" -ForegroundColor Gray
        foreach ($q in $result.quiz.questions) {
            Write-Host "   - $($q.question)" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "FAIL: Quiz error" -ForegroundColor Red
}
Write-Host ""

# Test 5: Learning Paths
Write-Host "Test 5: Learning Paths" -ForegroundColor Yellow
try {
    $result = Invoke-RestMethod -Uri "$baseUrl/api/path/all"
    if ($result.success) {
        Write-Host "PASS: Learning paths available!" -ForegroundColor Green
        Write-Host "   Paths:" -ForegroundColor Gray
        foreach ($path in $result.paths.PSObject.Properties) {
            $p = $path.Value
            Write-Host "   - $($p.name): $($p.total_lessons) lessons ($($p.estimated_weeks) weeks)" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "FAIL: Paths error" -ForegroundColor Red
}
Write-Host ""

# Test 6: Gamification
Write-Host "Test 6: Gamification System" -ForegroundColor Yellow
try {
    $result = Invoke-RestMethod -Uri "$baseUrl/api/gamification/summary?user_id=1"
    if ($result.success) {
        Write-Host "PASS: Gamification working!" -ForegroundColor Green
        if ($result.summary) {
            Write-Host "   Points: $($result.summary.total_points)" -ForegroundColor Gray
            Write-Host "   Level: $($result.summary.level)" -ForegroundColor Gray
            Write-Host "   Streak: $($result.summary.streak_days) days" -ForegroundColor Gray
        } else {
            Write-Host "   (No user data yet - system ready)" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "FAIL: Gamification error" -ForegroundColor Red
}
Write-Host ""

# Summary
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "ALL FEATURES TESTED!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server: $baseUrl" -ForegroundColor Cyan
Write-Host "Status: ONLINE" -ForegroundColor Green
Write-Host ""
Write-Host "Open in browser: $baseUrl" -ForegroundColor Yellow
Write-Host ""
