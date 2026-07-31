/* ============================================================
   Scroll Animation Engine
   IntersectionObserver-based reveal animations
   ============================================================ */

class ScrollAnimations {
    constructor() {
        this.observers = [];
        this.init();
    }

    init() {
        // Only initialize if reduced motion is not preferred
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            // Show all elements immediately
            document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale').forEach(el => {
                el.classList.add('revealed');
            });
            return;
        }

        this.setupRevealObserver();
        this.setupNavHighlight();
    }

    setupRevealObserver() {
        const options = {
            root: null,
            rootMargin: '0px 0px -80px 0px',
            threshold: 0.1,
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    // Don't unobserve stagger children parents
                    if (!entry.target.closest('.stagger-children') || 
                        entry.target.classList.contains('stagger-children')) {
                        // Keep observing for potential re-entry
                    }
                }
            });
        }, options);

        document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale').forEach(el => {
            observer.observe(el);
        });

        this.observers.push(observer);
    }

    setupNavHighlight() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-link');

        const options = {
            root: null,
            rootMargin: '-20% 0px -60% 0px',
            threshold: 0,
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.getAttribute('id');
                    navLinks.forEach(link => {
                        link.classList.toggle('active', link.getAttribute('data-section') === id);
                    });
                }
            });
        }, options);

        sections.forEach(section => observer.observe(section));
        this.observers.push(observer);
    }

    destroy() {
        this.observers.forEach(observer => observer.disconnect());
    }
}

// Defer initialization to idle time to minimize TBT
function initScrollAnimations() {
    window.scrollAnimations = new ScrollAnimations();
}
if ('requestIdleCallback' in window) {
    requestIdleCallback(initScrollAnimations, { timeout: 1500 });
} else {
    window.addEventListener('load', () => setTimeout(initScrollAnimations, 200));
}
