// Learnix Frontend - Chat Interface

const API_BASE = '/api';

// State
let isDarkMode = localStorage.getItem('theme') === 'dark';
let documents = [];

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const questionInput = document.getElementById('question-input');
const sendBtn = document.getElementById('send-btn');
const fileUpload = document.getElementById('file-upload');
const documentsList = document.getElementById('documents-list');
const sidebar = document.getElementById('sidebar');
const docsToggle = document.getElementById('docs-toggle');
const closeSidebar = document.getElementById('close-sidebar');
const themeToggle = document.getElementById('theme-toggle');
const statusText = document.getElementById('status-text');
const modeIndicator = document.getElementById('mode-indicator');
const clearChatBtn = document.getElementById('clear-chat');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    checkHealth();
    loadDocuments();
    loadChatHistory();
    setupEventListeners();
});

// Theme Management
function initTheme() {
    if (isDarkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
        themeToggle.textContent = '☀️';
    }
}

themeToggle.addEventListener('click', () => {
    isDarkMode = !isDarkMode;
    document.documentElement.setAttribute('data-theme', isDarkMode ? 'dark' : 'light');
    themeToggle.textContent = isDarkMode ? '☀️' : '🌙';
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
});

// Event Listeners
function setupEventListeners() {
    chatForm.addEventListener('submit', handleSubmit);
    fileUpload.addEventListener('change', handleFileUpload);
    docsToggle.addEventListener('click', toggleSidebar);
    closeSidebar.addEventListener('click', toggleSidebar);
    clearChatBtn.addEventListener('click', handleClearChat);
}

function toggleSidebar() {
    sidebar.classList.toggle('active');
}

// API Functions
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        
        if (data.status === 'ok') {
            statusText.textContent = 'Connected';
            modeIndicator.textContent = data.mode === 'mock' ? 'Mock Mode' : 'Production';
            modeIndicator.style.background = data.mode === 'mock' ? '#8b5cf6' : '#10b981';
        }
    } catch (error) {
        statusText.textContent = 'Connection Error';
        console.error('Health check failed:', error);
    }
}

async function loadDocuments() {
    try {
        const response = await fetch(`${API_BASE}/documents/`);
        const data = await response.json();
        documents = data.documents || [];
        renderDocuments();
    } catch (error) {
        console.error('Failed to load documents:', error);
    }
}

async function loadChatHistory() {
    try {
        const response = await fetch(`${API_BASE}/chat/history?limit=20`);
        const data = await response.json();
        
        if (data.history && data.history.length > 0) {
            // Remove welcome message if history exists
            const welcomeMsg = chatMessages.querySelector('.welcome-message');
            if (welcomeMsg) welcomeMsg.remove();
            
            // Render history messages
            data.history.forEach(msg => {
                addMessageFromHistory(msg.question, 'user', msg.timestamp);
                addMessageFromHistory(msg.answer, 'bot', msg.timestamp);
            });
            
            scrollToBottom();
        }
    } catch (error) {
        console.error('Failed to load chat history:', error);
    }
}

async function handleClearChat() {
    if (!confirm('Are you sure you want to clear all chat history? This cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/chat/history`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            // Clear UI
            chatMessages.innerHTML = `
                <div class="welcome-message">
                    <div class="welcome-icon">👋</div>
                    <h2>Welcome to Learnix!</h2>
                    <p>Upload your study materials and ask me anything.</p>
                    <div class="quick-tips">
                        <p><strong>Quick tips:</strong></p>
                        <ul>
                            <li>Upload PDFs, DOCX, or TXT files</li>
                            <li>Ask specific questions about your documents</li>
                            <li>I'll search through all uploaded materials</li>
                        </ul>
                    </div>
                </div>
            `;
            addSystemMessage('✅ Chat history cleared');
            setStatus('Chat history cleared');
        }
    } catch (error) {
        console.error('Failed to clear chat history:', error);
        addSystemMessage('❌ Failed to clear chat history');
    }
}

function renderDocuments() {
    if (documents.length === 0) {
        documentsList.innerHTML = '<p class="empty-state">No documents uploaded yet</p>';
        return;
    }

    documentsList.innerHTML = documents.map(doc => `
        <div class="document-item">
            <div class="doc-name">${escapeHtml(doc.name)}</div>
            <div class="doc-size">${formatFileSize(doc.size)}</div>
        </div>
    `).join('');
}

async function handleFileUpload(event) {
    const files = Array.from(event.target.files);
    
    if (files.length === 0) return;

    setStatus('Uploading files...');
    
    for (const file of files) {
        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${API_BASE}/upload/`, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (response.ok) {
                addSystemMessage(`✅ Uploaded: ${file.name}`);
            } else {
                addSystemMessage(`❌ Failed to upload ${file.name}: ${data.detail || 'Unknown error'}`);
            }
        } catch (error) {
            addSystemMessage(`❌ Error uploading ${file.name}: ${error.message}`);
        }
    }

    // Clear file input and reload documents
    event.target.value = '';
    await loadDocuments();
    setStatus('Ready');
}

async function handleSubmit(event) {
    event.preventDefault();

    const question = questionInput.value.trim();
    if (!question) return;

    // Clear input and disable send button
    questionInput.value = '';
    sendBtn.disabled = true;

    // Remove welcome message if present
    const welcomeMsg = chatMessages.querySelector('.welcome-message');
    if (welcomeMsg) welcomeMsg.remove();

    // Add user message
    addMessage(question, 'user');

    // Show typing indicator
    const typingId = addTypingIndicator();

    try {
        const formData = new FormData();
        formData.append('question', question);
        formData.append('top_k', '5');

        const response = await fetch(`${API_BASE}/ask/`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator(typingId);

        if (response.ok) {
            addMessage(data.answer, 'bot');
            setStatus(`Found ${data.sources?.length || 0} relevant sources`);
        } else {
            addMessage(`Error: ${data.detail || 'Failed to get answer'}`, 'bot');
        }
    } catch (error) {
        removeTypingIndicator(typingId);
        addMessage(`Error: ${error.message}`, 'bot');
    } finally {
        sendBtn.disabled = false;
        questionInput.focus();
    }
}

// Render Markdown to HTML
function renderMarkdown(text) {
    // Configure marked for GitHub-flavored markdown
    marked.setOptions({
        gfm: true,
        breaks: true,
        headerIds: false,
        mangle: false
    });
    
    // Convert markdown to HTML
    const html = marked.parse(text);
    
    // Create a temporary container to apply syntax highlighting
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;
    
    // Apply syntax highlighting to code blocks
    tempDiv.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
    });
    
    return tempDiv.innerHTML;
}

// UI Functions
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const timestamp = new Date().toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        hour12: true 
    });
    
    // Render AI messages with Markdown, user messages as plain text
    const content = sender === 'ai' ? renderMarkdown(text) : escapeHtml(text);
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-text">${content}</div>
            <div class="message-timestamp">${timestamp}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function addMessageFromHistory(text, sender, timestamp) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const date = new Date(timestamp);
    const timeStr = date.toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        hour12: true 
    });
    
    // Render AI messages with Markdown, user messages as plain text
    const content = sender === 'ai' ? renderMarkdown(text) : escapeHtml(text);
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-text">${escapeHtml(text)}</div>
            <div class="message-timestamp">${timeStr}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
}

function addSystemMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    messageDiv.innerHTML = `
        <div class="message-content" style="background: var(--bg-color); font-size: 0.9em;">
            <div class="message-text">${escapeHtml(text)}</div>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function addTypingIndicator() {
    const typingId = `typing-${Date.now()}`;
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot';
    typingDiv.id = typingId;
    
    typingDiv.innerHTML = `
        <div class="message-content">
            <div class="typing-indicator">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
    return typingId;
}

function removeTypingIndicator(typingId) {
    const element = document.getElementById(typingId);
    if (element) element.remove();
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function setStatus(text) {
    statusText.textContent = text;
}

// Utility Functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Enable Enter key to send (with Shift+Enter for new line)
questionInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        if (questionInput.value.trim()) {
            chatForm.dispatchEvent(new Event('submit'));
        }
    }
});
