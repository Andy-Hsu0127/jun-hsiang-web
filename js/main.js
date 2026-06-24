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
            
            // Lazy load target slide background
            const slide = slides[currentSlide];
            if (slide.dataset.bg && !slide.style.backgroundImage) {
                slide.style.backgroundImage = `url('${slide.dataset.bg}')`;
            }

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

        // Lazy load all remaining slides after page load (delay 2.5 seconds) to protect PageSpeed
        window.addEventListener('load', () => {
            setTimeout(() => {
                slides.forEach(slide => {
                    if (slide.dataset.bg && !slide.style.backgroundImage) {
                        slide.style.backgroundImage = `url('${slide.dataset.bg}')`;
                    }
                });
            }, 2500);
        });
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

    // Check URL query parameter for category
    const urlParams = new URLSearchParams(window.location.search);
    const catParam = urlParams.get('category');
    if (catParam) {
        const targetItem = Array.from(categoryItems).find(item => item.dataset.filter === catParam);
        if (targetItem) {
            // Wait slightly for DOM and reveal animations to settle
            setTimeout(() => {
                targetItem.click();
            }, 100);
        }
    }

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
    // ---- Glow Card Mouse Effects ----
    const glowCards = document.querySelectorAll('.glow-card');
    glowCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });

    // ---- RFP Option Cards Selection ----
    const optionCards = document.querySelectorAll('.rfp-option-card');
    optionCards.forEach(card => {
        card.addEventListener('click', () => {
            const grid = card.closest('.rfp-options-grid');
            if (!grid) return;
            const inputId = grid.dataset.inputId;
            const input = document.getElementById(inputId);
            if (input) {
                input.value = card.dataset.value;
            }
            
            // Toggle selection class
            grid.querySelectorAll('.rfp-option-card').forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
        });
    });

    // ---- RFP Wizard Navigation ----
    let rfpCurrentStep = 1;
    const rfpTotalSteps = 4;
    const rfpPrevBtn = document.getElementById('rfp-prev-btn');
    const rfpNextBtn = document.getElementById('rfp-next-btn');
    const rfpSubmitBtn = document.getElementById('rfp-submit-btn');
    const rfpProgressBar = document.getElementById('rfp-progress');
    const rfpStepDots = document.querySelectorAll('.rfp-step-dot');
    const rfpSteps = document.querySelectorAll('.rfp-step');

    function updateRFPWizard() {
        // Show/hide steps
        rfpSteps.forEach(step => {
            if (parseInt(step.dataset.step) === rfpCurrentStep) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });

        // Update step dots
        rfpStepDots.forEach(dot => {
            const stepNum = parseInt(dot.dataset.step);
            if (stepNum === rfpCurrentStep) {
                dot.classList.add('active');
                dot.classList.remove('completed');
            } else if (stepNum < rfpCurrentStep) {
                dot.classList.remove('active');
                dot.classList.add('completed');
            } else {
                dot.classList.remove('active');
                dot.classList.remove('completed');
            }
        });

        // Update Progress Bar
        const progressPercent = ((rfpCurrentStep - 1) / (rfpTotalSteps - 1)) * 100;
        if (rfpProgressBar) {
            rfpProgressBar.style.width = `${25 + progressPercent * 0.75}%`; // start at 25%, end at 100%
        }

        // Show/hide buttons
        if (rfpPrevBtn) {
            rfpPrevBtn.style.display = rfpCurrentStep > 1 ? 'block' : 'none';
        }
        if (rfpNextBtn) {
            rfpNextBtn.style.display = rfpCurrentStep < rfpTotalSteps ? 'block' : 'none';
        }
        if (rfpSubmitBtn) {
            rfpSubmitBtn.style.display = rfpCurrentStep === rfpTotalSteps ? 'block' : 'none';
        }
    }

    function validateRFPStep(step) {
        return true;
    }

    if (rfpNextBtn) {
        rfpNextBtn.addEventListener('click', () => {
            if (validateRFPStep(rfpCurrentStep)) {
                rfpCurrentStep++;
                updateRFPWizard();
            }
        });
    }

    if (rfpPrevBtn) {
        rfpPrevBtn.addEventListener('click', () => {
            rfpCurrentStep--;
            updateRFPWizard();
        });
    }

    // ---- RFP Form Submit Handler ----
    const rfpForm = document.getElementById('contact-form');
    if (rfpForm) {
        rfpForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Validate step 4 inputs
            const name = document.getElementById('rfp-name');
            const phone = document.getElementById('rfp-phone');
            const email = document.getElementById('rfp-email');

            if (!name.value.trim() && !phone.value.trim() && !email.value.trim()) {
                alert('請至少填寫聯絡人姓名、電話或 E-mail 其中一項，以便我們回覆您！');
                return;
            }

            // Disable button and show sending state
            const originalContent = rfpSubmitBtn.innerHTML;
            rfpSubmitBtn.innerHTML = '<span style="display:inline-flex;align-items:center;gap:8px;">傳送中...</span>';
            rfpSubmitBtn.disabled = true;

            // Use FormData to allow file uploads
            const formData = new FormData(rfpForm);
            const actionUrl = rfpForm.getAttribute('action') || "https://formsubmit.co/ajax/jojo.li888@msa.hinet.net";

            fetch(actionUrl, {
                method: "POST",
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    // Success animation
                    rfpSubmitBtn.innerHTML = '<span style="display:inline-flex;align-items:center;gap:8px;">✓ 詢價單已成功送出</span>';
                    rfpSubmitBtn.style.background = 'linear-gradient(135deg, #2ECC71, #27AE60)';
                    
                    setTimeout(() => {
                        rfpForm.reset();
                        // Reset option cards selection
                        document.querySelectorAll('.rfp-option-card').forEach(c => c.classList.remove('selected'));
                        // Go back to step 1
                        rfpCurrentStep = 1;
                        updateRFPWizard();
                        
                        rfpSubmitBtn.innerHTML = originalContent;
                        rfpSubmitBtn.style.background = '';
                        rfpSubmitBtn.disabled = false;
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
                rfpSubmitBtn.innerHTML = '<span style="display:inline-flex;align-items:center;gap:8px;">❌ 傳送失敗，請重試</span>';
                rfpSubmitBtn.style.background = 'linear-gradient(135deg, #E74C3C, #C0392B)';
                
                setTimeout(() => {
                    rfpSubmitBtn.innerHTML = originalContent;
                    rfpSubmitBtn.style.background = '';
                    rfpSubmitBtn.disabled = false;
                    if (typeof lucide !== 'undefined') {
                        lucide.createIcons();
                    }
                }, 3000);
            });
        });
    }

    // ---- Material Selection Helper Interaction ----
    const materialHelper = document.getElementById('material-results');
    if (materialHelper) {
        const checkboxes = document.querySelectorAll('.material-checkbox-input');
        const cards = document.querySelectorAll('.material-result-card');
        const emptyState = document.getElementById('material-helper-empty');

        function filterMaterials() {
            // Get all checked values
            const activeProps = [];
            checkboxes.forEach(cb => {
                const label = cb.closest('.material-checkbox-label');
                if (cb.checked) {
                    activeProps.push(cb.value);
                    if (label) label.classList.add('checked');
                } else {
                    if (label) label.classList.remove('checked');
                }
            });

            let visibleCount = 0;

            cards.forEach(card => {
                const cardTags = card.dataset.tags ? card.dataset.tags.split(',') : [];
                
                if (activeProps.length === 0) {
                    // Show all cards when no checkbox is checked
                    card.classList.remove('hidden');
                    visibleCount++;
                } else {
                    // Check if card matches AT LEAST ONE selected property (OR match)
                    const isMatch = activeProps.some(prop => cardTags.includes(prop));
                    if (isMatch) {
                        card.classList.remove('hidden');
                        visibleCount++;
                    } else {
                        card.classList.add('hidden');
                    }
                }
            });

            // Show empty state if no matches
            if (visibleCount === 0 && emptyState) {
                emptyState.classList.remove('hidden');
            } else if (emptyState) {
                emptyState.classList.add('hidden');
            }
        }

        checkboxes.forEach(cb => {
            cb.addEventListener('change', filterMaterials);
        });

        // Initial run to format correctly
        filterMaterials();
    }
    // ---- Contact Tabs Switcher ----
    const contactTabButtons = document.querySelectorAll('.contact-tabs .tab-btn');
    const contactTabContents = document.querySelectorAll('.contact-form-tab-content');

    contactTabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            contactTabButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            contactTabContents.forEach(content => {
                content.style.display = 'none';
                content.classList.remove('active');
            });

            const tabId = btn.dataset.tab;
            const targetContent = document.getElementById(`${tabId}-contact-content`);
            if (targetContent) {
                targetContent.style.display = 'block';
                targetContent.classList.add('active');
            }
        });
    });

    // ---- General Contact Form Submit Handler ----
    const generalForm = document.getElementById('general-contact-form');
    const generalSubmitBtn = document.getElementById('general-submit-btn');
    if (generalForm && generalSubmitBtn) {
        generalForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const name = document.getElementById('general-name');
            const phone = document.getElementById('general-phone');
            const email = document.getElementById('general-email');
            
            if (!name.value.trim() && !phone.value.trim() && !email.value.trim()) {
                alert('請至少填寫聯絡人姓名、電話或 E-mail 其中一項，以便我們回覆您！');
                return;
            }

            const originalContent = generalSubmitBtn.innerHTML;
            generalSubmitBtn.innerHTML = '<span style="display:inline-flex;align-items:center;gap:8px;">傳送中...</span>';
            generalSubmitBtn.disabled = true;

            const formData = new FormData(generalForm);
            const actionUrl = generalForm.getAttribute('action') || "https://formsubmit.co/ajax/jojo.li888@msa.hinet.net";

            fetch(actionUrl, {
                method: "POST",
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    generalSubmitBtn.innerHTML = '<span style="display:inline-flex;align-items:center;gap:8px;">✓ 訊息已成功送出</span>';
                    generalSubmitBtn.style.background = 'linear-gradient(135deg, #2ECC71, #27AE60)';
                    
                    setTimeout(() => {
                        generalForm.reset();
                        generalSubmitBtn.innerHTML = originalContent;
                        generalSubmitBtn.style.background = '';
                        generalSubmitBtn.disabled = false;
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
                generalSubmitBtn.innerHTML = '<span style="display:inline-flex;align-items:center;gap:8px;">❌ 傳送失敗，請重試</span>';
                generalSubmitBtn.style.background = 'linear-gradient(135deg, #E74C3C, #C0392B)';
                
                setTimeout(() => {
                    generalSubmitBtn.innerHTML = originalContent;
                    generalSubmitBtn.style.background = '';
                    generalSubmitBtn.disabled = false;
                    if (typeof lucide !== 'undefined') {
                        lucide.createIcons();
                    }
                }, 3000);
            });
        });
    }
});
