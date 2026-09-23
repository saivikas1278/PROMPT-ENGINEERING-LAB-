document.addEventListener("DOMContentLoaded", () => {
    
    // Toast Notification System
    window.showToast = function(message, type = 'success') {
        const container = document.getElementById('toast-container');
        if (!container) return;
        
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        let icon = '';
        if (type === 'success') icon = '✓';
        else if (type === 'error') icon = '✕';
        else if (type === 'warning') icon = '⚠';
        
        toast.innerHTML = `
            <div class="toast-icon">${icon}</div>
            <div class="toast-message">${message}</div>
        `;
        
        container.appendChild(toast);
        
        // Trigger reflow to ensure transition runs
        toast.offsetHeight;
        
        toast.classList.add('show');
        
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                toast.remove();
            }, 300); // Wait for transition to finish
        }, 3000);
    };

    // Swap Source and Destination on Home Form
    const swapBtn = document.getElementById('swap-locations');
    if (swapBtn) {
        swapBtn.addEventListener('click', () => {
            const sourceSelect = document.getElementById('source');
            const destSelect = document.getElementById('destination');
            
            if (sourceSelect && destSelect) {
                const temp = sourceSelect.value;
                sourceSelect.value = destSelect.value;
                destSelect.value = temp;
            }
        });
    }

    // Home Form Validation and Loading State
    const searchForm = document.getElementById('search-form-home');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const source = document.getElementById('source').value;
            const dest = document.getElementById('destination').value;
            
            if (!source) {
                e.preventDefault();
                showToast('Please select a starting location.', 'error');
                return;
            }
            if (!dest) {
                e.preventDefault();
                showToast('Please select a destination.', 'error');
                return;
            }
            
            if (source === dest) {
                e.preventDefault();
                showToast('Source and destination cannot be the same.', 'warning');
                return;
            }
            
            // Show loading state
            const submitBtn = document.getElementById('search-submit-btn');
            const loadingState = document.getElementById('loading-state');
            
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span>Searching...</span>';
            
            if (loadingState) {
                loadingState.style.display = 'block';
                // Hide search layout to show just the spinner
                document.querySelector('.search-layout').style.opacity = '0.5';
                document.querySelector('.search-layout').style.pointerEvents = 'none';
            }
        });
    }
});
