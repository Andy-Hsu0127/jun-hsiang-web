/* ============================================================
   Counter Animation
   Animated number counter triggered by scroll
   ============================================================ */

class CounterAnimation {
    constructor() {
        this.counters = [];
        this.init();
    }

    init() {
        const elements = document.querySelectorAll('.counter');
        if (!elements.length) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.dataset.counted) {
                    entry.target.dataset.counted = 'true';
                    this.animateCounter(entry.target);
                }
            });
        }, { threshold: 0.5 });

        elements.forEach(el => observer.observe(el));
    }

    animateCounter(element) {
        const target = parseFloat(element.dataset.target);
        const duration = 2000;
        const startTime = performance.now();
        const isDecimal = target % 1 !== 0;

        const update = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Ease out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = eased * target;

            if (isDecimal) {
                element.textContent = current.toFixed(1);
            } else {
                element.textContent = Math.floor(current).toLocaleString();
            }

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                if (isDecimal) {
                    element.textContent = target.toFixed(1);
                } else {
                    element.textContent = target.toLocaleString();
                }
            }
        };

        requestAnimationFrame(update);
    }
}

// Also animate hero stat numbers
class HeroStatCounter {
    constructor() {
        this.init();
    }

    init() {
        const heroStats = document.querySelectorAll('.hero-stat .stat-number[data-count]');
        heroStats.forEach(stat => {
            const target = parseInt(stat.dataset.count);
            if (!target) return;

            // Delay to sync with hero animation
            setTimeout(() => {
                this.animate(stat, target);
            }, 1800);
        });
    }

    animate(element, target) {
        const duration = 2000;
        const startTime = performance.now();
        const suffix = target >= 100 ? '+' : '+';

        const update = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(eased * target);

            element.textContent = current.toLocaleString() + suffix;

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                element.textContent = target.toLocaleString() + suffix;
            }
        };

        requestAnimationFrame(update);
    }
}

// Defer initialization to idle time to minimize TBT
function initCounters() {
    window.counterAnimation = new CounterAnimation();
    window.heroStatCounter = new HeroStatCounter();
}
if ('requestIdleCallback' in window) {
    requestIdleCallback(initCounters, { timeout: 2000 });
} else {
    window.addEventListener('load', () => setTimeout(initCounters, 300));
}
