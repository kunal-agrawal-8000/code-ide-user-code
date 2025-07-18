// Twitter Clone JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Character counter for tweet composer
    const tweetTextarea = document.querySelector('textarea[name="content"]');
    if (tweetTextarea) {
        const maxLength = 280;
        
        // Create character counter
        const counterElement = document.createElement('span');
        counterElement.className = 'char-counter';
        counterElement.textContent = maxLength;
        
        // Find the submit button's parent and add counter
        const submitButton = tweetTextarea.closest('form').querySelector('button[type="submit"]');
        const counterContainer = submitButton.parentElement;
        const existingCounter = counterContainer.querySelector('.text-muted');
        
        if (existingCounter) {
            existingCounter.appendChild(counterElement);
        }
        
        // Update character count
        tweetTextarea.addEventListener('input', function() {
            const remaining = maxLength - this.value.length;
            counterElement.textContent = remaining;
            
            // Update counter styling
            counterElement.className = 'char-counter';
            if (remaining < 20) {
                counterElement.classList.add('warning');
            }
            if (remaining < 0) {
                counterElement.classList.add('danger');
                submitButton.disabled = true;
            } else {
                submitButton.disabled = false;
            }
        });
    }
    
    // Auto-refresh timeline (every 30 seconds)
    if (window.location.pathname === '/') {
        setInterval(function() {
            // Only refresh if user is on home page and not actively typing
            if (document.activeElement !== tweetTextarea) {
                refreshTimeline();
            }
        }, 30000);
    }
    
    // Smooth scrolling for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            if (alert.classList.contains('show')) {
                alert.classList.remove('show');
                setTimeout(() => alert.remove(), 150);
            }
        });
    }, 5000);
});

// Function to refresh timeline
function refreshTimeline() {
    fetch('/api/tweets')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error fetching tweets:', data.error);
                return;
            }
            
            // Update timeline with new tweets
            const timeline = document.querySelector('.card-body');
            if (timeline && data.length > 0) {
                // For now, just log that we would update
                console.log('Timeline would be updated with', data.length, 'tweets');
            }
        })
        .catch(error => {
            console.error('Error refreshing timeline:', error);
        });
}

// Function to format timestamps
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) {
        return `${diffInSeconds}s`;
    } else if (diffInSeconds < 3600) {
        return `${Math.floor(diffInSeconds / 60)}m`;
    } else if (diffInSeconds < 86400) {
        return `${Math.floor(diffInSeconds / 3600)}h`;
    } else {
        return date.toLocaleDateString();
    }
}

// Function to handle tweet actions (like, retweet, etc.)
function handleTweetAction(action, tweetId) {
    // Placeholder for future tweet actions
    console.log(`${action} action on tweet ${tweetId}`);
}

// Function to show loading state
function showLoading(element) {
    element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    element.disabled = true;
}

// Function to hide loading state
function hideLoading(element, originalText) {
    element.innerHTML = originalText;
    element.disabled = false;
}