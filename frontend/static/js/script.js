/**
 * Public Transport & Route Assistant
 * Frontend UI Interactions & Enhancements
 */

document.addEventListener("DOMContentLoaded", () => {
    // 1. Mobile Navigation Toggle
    const navToggle = document.getElementById("mobile-menu-toggle");
    const navLinks = document.getElementById("nav-links");
    
    if (navToggle && navLinks) {
        navToggle.addEventListener("click", () => {
            navLinks.classList.toggle("active");
            // Optional: Toggle icon between menu and x
            const icon = navToggle.querySelector("i");
            if (navLinks.classList.contains("active")) {
                icon.setAttribute("data-lucide", "x");
            } else {
                icon.setAttribute("data-lucide", "menu");
            }
            if (window.lucide) window.lucide.createIcons();
        });
    }

    // 2. Form Swap Button (Home Page)
    const swapBtn = document.getElementById("swap-btn");
    const sourceSelect = document.getElementById("source");
    const destSelect = document.getElementById("destination");
    
    if (swapBtn && sourceSelect && destSelect) {
        swapBtn.addEventListener("click", (e) => {
            e.preventDefault();
            const temp = sourceSelect.value;
            sourceSelect.value = destSelect.value;
            destSelect.value = temp;
            
            // Add subtle rotation animation to the icon
            swapBtn.style.transform = "rotate(180deg)";
            setTimeout(() => {
                swapBtn.style.transition = "none";
                swapBtn.style.transform = "rotate(0deg)";
                setTimeout(() => swapBtn.style.transition = "all 0.15s ease-in-out", 10);
            }, 150);
        });
    }

    // 3. Search Form Validation & Loading State
    const searchForm = document.getElementById("search-form");
    if (searchForm) {
        searchForm.addEventListener("submit", (e) => {
            if (!sourceSelect || !destSelect) return;
            
            if (sourceSelect.value === destSelect.value && sourceSelect.value !== "") {
                e.preventDefault();
                showToast("Source and destination cannot be the same.", "warning");
                return;
            }
            
            // Add loading state to button
            const submitBtn = searchForm.querySelector("button[type='submit']");
            if (submitBtn) {
                submitBtn.classList.add("loading");
                submitBtn.innerHTML = `<span class="spinner"></span> Finding routes...`;
            }
        });
    }

    // 4. Initialize Lucide Icons
    if (window.lucide) {
        window.lucide.createIcons();
    }
});

/**
 * Toast Notification System
 * @param {string} message - The message to display
 * @param {string} type - 'success', 'error', 'warning', 'info'
 */
function showToast(message, type = "info") {
    let container = document.getElementById("toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        container.className = "toast-container";
        document.body.appendChild(container);
    }
    
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    
    let iconName = "info";
    if (type === "success") iconName = "check-circle";
    if (type === "error") iconName = "alert-circle";
    if (type === "warning") iconName = "alert-triangle";

    toast.innerHTML = `
        <i data-lucide="${iconName}" class="toast-icon"></i>
        <div class="toast-content">${message}</div>
        <button class="toast-close"><i data-lucide="x" style="width: 16px; height: 16px;"></i></button>
    `;
    
    container.appendChild(toast);
    
    // Re-render icons for this toast
    if (window.lucide) window.lucide.createIcons({ root: toast });
    
    // Trigger animation
    setTimeout(() => toast.classList.add("show"), 10);
    
    // Close handler
    const closeBtn = toast.querySelector(".toast-close");
    const removeToast = () => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 300); // Wait for transition
    };
    
    closeBtn.addEventListener("click", removeToast);
    
    // Auto remove after 5 seconds
    setTimeout(removeToast, 5000);
}
