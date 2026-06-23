/* ============================================================
   Main Application Logic
   Navigation, Loading, Product Filter, Interactions
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
    // ---- Initialize Lucide Icons ----
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // ---- Loading Screen ----
    const loadingScreen = document.getElementById('loading-screen');
    const hero = document.querySelector('.hero');

    setTimeout(() => {
        if (loadingScreen) {
            loadingScreen.classList.add('hide');
            // Initialize Particles earlier
            if (window.initHeroParticles) {
                window.initHeroParticles('hero-canvas');
            }
            // Trigger hero animations
            setTimeout(() => {
                if (hero) hero.classList.add('loaded');
            }, 200);
            // Remove loading screen from DOM
            setTimeout(() => {
                loadingScreen.remove();
            }, 1000);
        }
    }, 800); 

    // ---- Navbar Scroll Effects ----
    const navbar = document.getElementById('navbar');
    let lastScrollY = 0;
    let ticking = false;

    function updateNavbar() {
        const scrollY = window.scrollY;

        // Add scrolled class
        if (scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        // Hide/show navbar on scroll direction (only on desktop)
        if (window.innerWidth > 768) {
            if (scrollY > lastScrollY && scrollY > 400) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }
        }

        lastScrollY = scrollY;
        ticking = false;
    }

    if (navbar) {
        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(updateNavbar);
                ticking = true;
            }
        });
    }

    // ---- Hamburger Menu ----
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobile-menu');

    if (hamburger && mobileMenu) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            mobileMenu.classList.toggle('active');
            document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
        });

        // Close mobile menu on link click
        mobileMenu.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                mobileMenu.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }

    // ---- Hero Carousel ----
    const slides = document.querySelectorAll('.hero-slide');
    const dotsContainer = document.getElementById('hero-dots');
    const prevBtn = document.getElementById('hero-prev');
    const nextBtn = document.getElementById('hero-next');
    let currentSlide = 0;
    let slideInterval;

    if (slides.length > 0 && dotsContainer && prevBtn && nextBtn) {
        // Create dots
        slides.forEach((_, index) => {
            const dot = document.createElement('span');
            dot.classList.add('dot');
            if (index === 0) dot.classList.add('active');
            dot.dataset.slide = index;
            dot.addEventListener('click', () => goToSlide(index));
            dotsContainer.appendChild(dot);
        });

        const dots = document.querySelectorAll('.dot');

        function goToSlide(index) {
            slides[currentSlide].classList.remove('active');
            dots[currentSlide].classList.remove('active');
            currentSlide = (index + slides.length) % slides.length;
            slides[currentSlide].classList.add('active');
            dots[currentSlide].classList.add('active');
            resetInterval();
        }

        prevBtn.addEventListener('click', () => goToSlide(currentSlide - 1));
        nextBtn.addEventListener('click', () => goToSlide(currentSlide + 1));

        function nextSlide() { goToSlide(currentSlide + 1); }
        function resetInterval() {
            clearInterval(slideInterval);
            slideInterval = setInterval(nextSlide, 5000);
        }
        resetInterval();
    }

    // ---- Product Filter (Sidebar) ----
    const categoryItems = document.querySelectorAll('.category-item');
    const productCards = document.querySelectorAll('.product-card');

    categoryItems.forEach(item => {
        item.addEventListener('click', () => {
            categoryItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');

            const filter = item.dataset.filter;

            productCards.forEach(card => {
                if (filter === 'all' || card.dataset.category === filter) {
                    card.style.display = '';
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.9)';
                    requestAnimationFrame(() => {
                        card.style.transition = 'all 0.4s cubic-bezier(0.16, 1, 0.3, 1)';
                        card.style.opacity = '1';
                        card.style.transform = 'scale(1)';
                    });
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.9)';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 300);
                }
            });
        });
    });

    // ---- Back to Top Button ----
    const backToTop = document.getElementById('back-to-top');
    if (backToTop) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 500) {
                backToTop.classList.add('show');
            } else {
                backToTop.classList.remove('show');
            }
        });

        backToTop.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // ---- Smooth Scroll for anchor links ----
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const navHeader = document.querySelector('.navbar');
                const offset = target.offsetTop - (navHeader ? navHeader.offsetHeight : 0);
                window.scrollTo({
                    top: offset,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ---- Product Modal System ----
    const modal = document.getElementById('product-modal');
    const modalClose = document.getElementById('modal-close');
    const modalBackdrop = document.getElementById('modal-backdrop');

    function openModal(card) {
        if (!modal) return;
        
        // Fill data
        document.getElementById('modal-title').textContent = card.dataset.title || '';
        document.getElementById('modal-title-small').textContent = card.dataset.title || '';
        document.getElementById('modal-category-text').textContent = card.dataset.type || '';
        document.getElementById('modal-desc').textContent = card.dataset.desc || '';
        document.getElementById('modal-img').src = card.dataset.img || '';

        // Show modal
        modal.classList.add('show');
        document.body.style.overflow = 'hidden'; // prevent background scrolling
        
        // Re-initialize icons if needed inside modal
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    function closeModal() {
        if (!modal) return;
        modal.classList.remove('show');
        document.body.style.overflow = '';
    }

    if (modal) {
        if (modalClose) modalClose.addEventListener('click', closeModal);
        if (modalBackdrop) modalBackdrop.addEventListener('click', closeModal);
        
        // Attach click to all product cards
        document.querySelectorAll('.product-card').forEach(card => {
            card.addEventListener('click', () => openModal(card));
            
            // Magnetic Tilt Effect
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                // Update CSS variables for light effect
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
                
                // Calculate Tilt (More sensitive)
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;
                
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
    }
    
    // Export closeModal to window for inline onclick usage if any
    window.closeModal = closeModal;

    // ---- FAQ Accordion Toggle ----
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        if (question) {
            question.addEventListener('click', () => {
                const isActive = item.classList.contains('active');
                
                // Close other items
                faqItems.forEach(otherItem => {
                    otherItem.classList.remove('active');
                });
                
                // Toggle current item
                if (!isActive) {
                    item.classList.add('active');
                }
            });
        }
    });
});

// ---- Contact Form Handler (Global) ----
function handleSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const submitBtn = form.querySelector('.btn-submit');
    
    // Disable button and show sending state
    const originalContent = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span style="display:inline-flex;align-items:center;gap:8px;">傳送中...</span>';
    submitBtn.disabled = true;

    // FormSubmit AJAX submission to jojo.li888@msa.hinet.net
    fetch("https://formsubmit.co/ajax/jojo.li888@msa.hinet.net", {
        method: "POST",
        headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            "公司名稱": form.elements["company"] ? form.elements["company"].value : "",
            "聯絡人": form.elements["contact-name"] ? form.elements["contact-name"].value : "",
            "電話": form.elements["phone"] ? form.elements["phone"].value : "",
            "E-mail": form.elements["email"] ? form.elements["email"].value : "",
            "產品需求": form.elements["product-need"] ? form.elements["product-need"].value : "",
            "留言內容": form.elements["message"] ? form.elements["message"].value : ""
        })
    })
    .then(response => {
        if (response.ok) {
            // Success animation
            submitBtn.innerHTML = '<span style="display:inline-flex;align-items:center;gap:8px;">✓ 已送出</span>';
            submitBtn.style.background = 'linear-gradient(135deg, #2ECC71, #27AE60)';
            
            setTimeout(() => {
                form.reset();
                submitBtn.innerHTML = originalContent;
                submitBtn.style.background = '';
                submitBtn.disabled = false;
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            }, 3000);
        } else {
            throw new Error("Form submission failed");
        }
    })
    .catch(error => {
        console.error(error);
        submitBtn.innerHTML = '<span style="display:inline-flex;align-items:center;gap:8px;">❌ 傳送失敗</span>';
        submitBtn.style.background = 'linear-gradient(135deg, #E74C3C, #C0392B)';
        
        setTimeout(() => {
            submitBtn.innerHTML = originalContent;
            submitBtn.style.background = '';
            submitBtn.disabled = false;
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }, 3000);
    });
}
