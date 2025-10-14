// Chicago World's Fair - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {

    // Mobile Menu Toggle
    const mobileMenuButton = document.querySelector('[data-mobile-menu-button]');
    const mobileMenu = document.querySelector('[data-mobile-menu]');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Sticky Header Shadow on Scroll
    const stickyHeader = document.querySelector('header.sticky, header.fixed');
    if (stickyHeader) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 10) {
                stickyHeader.classList.add('scrolled');
            } else {
                stickyHeader.classList.remove('scrolled');
            }
        });
    }

    // Form Progress Bar Update
    const formSteps = document.querySelectorAll('[data-form-step]');
    const progressBar = document.querySelector('.progress-bar');

    if (formSteps.length > 0 && progressBar) {
        updateProgressBar();
    }

    function updateProgressBar() {
        const currentStep = document.querySelector('[data-form-step].active');
        if (currentStep && progressBar) {
            const stepIndex = Array.from(formSteps).indexOf(currentStep);
            const progress = ((stepIndex + 1) / formSteps.length) * 100;
            progressBar.style.width = progress + '%';
        }
    }

    // File Upload Drag & Drop
    const uploadZones = document.querySelectorAll('.upload-zone, [data-upload-zone]');

    uploadZones.forEach(zone => {
        zone.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragging');
        });

        zone.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('dragging');
        });

        zone.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragging');

            const files = e.dataTransfer.files;
            handleFiles(files);
        });
    });

    function handleFiles(files) {
        console.log('Files uploaded:', files);
        // Handle file upload logic here
        // This will be connected to backend later
    }

    // Event Schedule - Add to Schedule Button
    const addToScheduleButtons = document.querySelectorAll('[data-add-to-schedule]');

    addToScheduleButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const eventId = this.dataset.eventId;
            toggleEventSchedule(eventId, this);
        });
    });

    function toggleEventSchedule(eventId, button) {
        const isAdded = button.classList.contains('added');

        if (isAdded) {
            button.classList.remove('added');
            button.innerHTML = '<span class="material-symbols-outlined">add_circle_outline</span> Add to Schedule';
            // Remove from schedule logic
        } else {
            button.classList.add('added');
            button.innerHTML = '<span class="material-symbols-outlined">check_circle</span> Added to Schedule';
            // Add to schedule logic
        }
    }

    // Calendar Date Selection
    const calendarDays = document.querySelectorAll('.calendar-day');

    calendarDays.forEach(day => {
        day.addEventListener('click', function() {
            calendarDays.forEach(d => d.classList.remove('selected'));
            this.classList.add('selected');

            const date = this.dataset.date;
            loadEventsForDate(date);
        });
    });

    function loadEventsForDate(date) {
        console.log('Loading events for:', date);
        // Load events for selected date
        // This will connect to backend later
    }

    // Search Functionality
    const searchInputs = document.querySelectorAll('input[type="search"], input[placeholder*="Search"]');

    searchInputs.forEach(input => {
        input.addEventListener('input', debounce(function(e) {
            const query = e.target.value;
            performSearch(query);
        }, 300));
    });

    function performSearch(query) {
        if (query.length < 2) return;
        console.log('Searching for:', query);
        // Search logic here
        // This will connect to backend later
    }

    // Debounce utility function
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Form Validation
    const forms = document.querySelectorAll('form[data-validate]');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });

    function validateForm(form) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                showError(field, 'This field is required');
            } else {
                clearError(field);
            }
        });

        return isValid;
    }

    function showError(field, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message text-red-500 text-sm mt-1';
        errorDiv.textContent = message;

        const existingError = field.parentElement.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        field.parentElement.appendChild(errorDiv);
        field.classList.add('border-red-500');
    }

    function clearError(field) {
        const errorDiv = field.parentElement.querySelector('.error-message');
        if (errorDiv) {
            errorDiv.remove();
        }
        field.classList.remove('border-red-500');
    }

    // Smooth Scroll for Anchor Links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');

    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Image Lazy Loading
    const lazyImages = document.querySelectorAll('img[data-src]');

    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    img.setAttribute('data-loaded', 'true');
                    observer.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => imageObserver.observe(img));
    }

    // Dark Mode Toggle (if you add a toggle button)
    const darkModeToggle = document.querySelector('[data-dark-mode-toggle]');

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.documentElement.classList.toggle('dark');
            const isDark = document.documentElement.classList.contains('dark');
            localStorage.setItem('darkMode', isDark);
        });

        // Check saved preference
        const savedDarkMode = localStorage.getItem('darkMode');
        if (savedDarkMode === 'true') {
            document.documentElement.classList.add('dark');
        }
    }

    // Tooltip Initialization
    const tooltipElements = document.querySelectorAll('[data-tooltip]');

    tooltipElements.forEach(el => {
        el.classList.add('tooltip');
    });

    // Print Page Functionality
    const printButtons = document.querySelectorAll('[data-print]');

    printButtons.forEach(button => {
        button.addEventListener('click', function() {
            window.print();
        });
    });

    // Filter/Checkbox Toggle for Exhibits Page
    const filterCheckboxes = document.querySelectorAll('input[type="checkbox"][data-filter]');

    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            applyFilters();
        });
    });

    function applyFilters() {
        const activeFilters = [];
        filterCheckboxes.forEach(cb => {
            if (cb.checked) {
                activeFilters.push(cb.dataset.filter);
            }
        });
        console.log('Active filters:', activeFilters);
        // Apply filtering logic here
    }

    // Registration Form - Character Counter
    const textareas = document.querySelectorAll('textarea[maxlength]');

    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        if (maxLength) {
            const counter = document.createElement('div');
            counter.className = 'text-sm text-gray-500 mt-1 text-right';
            counter.textContent = `0 / ${maxLength}`;
            textarea.parentElement.appendChild(counter);

            textarea.addEventListener('input', function() {
                const length = this.value.length;
                counter.textContent = `${length} / ${maxLength}`;
            });
        }
    });

    // Navigation Active State
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav a');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active', 'text-primary');
        }
    });

    console.log('Chicago World\'s Fair - Scripts Loaded Successfully');
});

// Utility: Format Date for Display
function formatDate(date) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(date).toLocaleDateString('en-US', options);
}

// Utility: Generate Unique ID
function generateId() {
    return 'id_' + Math.random().toString(36).substr(2, 9);
}

// Export functions for use in other scripts if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        formatDate,
        generateId
    };
}