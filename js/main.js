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

    // ---- Form Validation & Translation Dictionary ----
    const lang = window.location.pathname.includes('/en/') ? 'en' : (window.location.pathname.includes('/ja/') ? 'ja' : 'zh');

    const translations = {
        zh: {
            nameRequired: '請輸入聯絡人姓名',
            contactRequired: '請提供電話或 E-mail，以便我們回覆您',
            emailInvalid: '請輸入正確的 E-mail 格式',
            phoneInvalid: '請輸入有效的電話號碼格式',
            submitting: '傳送中...',
            submitSuccessTitle: '訊息已成功送出！',
            submitSuccessDesc: '感謝您的來信，我們將盡速安排專人與您聯絡。',
            submitFailTitle: '傳送失敗',
            submitFailDesc: '抱歉，系統目前無法處理您的請求，請直接來電或稍後重試。',
            close: '關閉'
        },
        en: {
            nameRequired: 'Please enter your name',
            contactRequired: 'Please provide either a phone number or email',
            emailInvalid: 'Please enter a valid email address',
            phoneInvalid: 'Please enter a valid phone number',
            submitting: 'Sending...',
            submitSuccessTitle: 'Message Sent Successfully!',
            submitSuccessDesc: 'Thank you for your message. Our representative will contact you as soon as possible.',
            submitFailTitle: 'Submission Failed',
            submitFailDesc: 'Sorry, we are unable to process your request at this time. Please call us directly or try again later.',
            close: 'Close'
        },
        ja: {
            nameRequired: 'お名前をご入力ください',
            contactRequired: 'ご連絡先（電話番号またはメール）をご入力ください',
            emailInvalid: '正しいメールアドレスの形式でご入力ください',
            phoneInvalid: '正しい電話番号の形式でご入力ください',
            submitting: '送信中...',
            submitSuccessTitle: '送信が完了しました！',
            submitSuccessDesc: 'お問い合わせいただきありがとうございます。担当者より折り返しご連絡いたします。',
            submitFailTitle: '送信失敗',
            submitFailDesc: '申し訳ありませんが、現在リクエストを処理できません。お電話いただくか、時間をおいて再度お試しください。',
            close: '閉じる'
        }
    };
    const t = translations[lang];

    function validateEmail(emailVal) {
        if (!emailVal) return true;
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(emailVal.trim());
    }

    function validatePhone(phoneVal) {
        if (!phoneVal) return true;
        // Allow digits, spaces, dashes, parentheses, plus sign. Length >= 6
        const re = /^[\d\s()+\-]+$/;
        return re.test(phoneVal.trim()) && phoneVal.trim().replace(/[^\d]/g, '').length >= 6;
    }

    function setError(inputEl, msg) {
        const group = inputEl.closest('.form-group');
        if (group) {
            group.classList.add('error');
            let errorMsg = group.querySelector('.error-message');
            if (!errorMsg) {
                errorMsg = document.createElement('div');
                errorMsg.className = 'error-message';
                group.appendChild(errorMsg);
            }
            errorMsg.textContent = msg;
        }
    }

    function clearError(inputEl) {
        const group = inputEl.closest('.form-group');
        if (group) {
            group.classList.remove('error');
        }
    }

    // Interactive Field Validation
    function validateField(inputEl) {
        clearError(inputEl);
        const id = inputEl.id;
        const val = inputEl.value.trim();

        if (id === 'general-name' || id === 'rfp-name') {
            if (!val) {
                setError(inputEl, t.nameRequired);
                return false;
            }
        }

        if (id === 'general-email' || id === 'rfp-email') {
            if (val && !validateEmail(val)) {
                setError(inputEl, t.emailInvalid);
                return false;
            }
        }

        if (id === 'general-phone' || id === 'rfp-phone') {
            if (val && !validatePhone(val)) {
                setError(inputEl, t.phoneInvalid);
                return false;
            }
        }

        // Check if both are empty (either general or rfp)
        const isGeneral = id.startsWith('general-');
        const phoneId = isGeneral ? 'general-phone' : 'rfp-phone';
        const emailId = isGeneral ? 'general-email' : 'rfp-email';
        const phoneEl = document.getElementById(phoneId);
        const emailEl = document.getElementById(emailId);

        if (phoneEl && emailEl && (id === phoneId || id === emailId)) {
            const phoneVal = phoneEl.value.trim();
            const emailVal = emailEl.value.trim();

            if (!phoneVal && !emailVal) {
                setError(phoneEl, t.contactRequired);
                setError(emailEl, t.contactRequired);
                return false;
            } else {
                // Clear the generic contactRequired error if at least one is filled,
                // but preserve specific format error if invalid.
                if (id === phoneId) {
                    clearError(emailEl);
                    if (emailVal && !validateEmail(emailVal)) {
                        setError(emailEl, t.emailInvalid);
                    }
                } else if (id === emailId) {
                    clearError(phoneEl);
                    if (phoneVal && !validatePhone(phoneVal)) {
                        setError(phoneEl, t.phoneInvalid);
                    }
                }
            }
        }

        return true;
    }

    // Attach real-time validation listeners
    const formInputs = document.querySelectorAll('.form-group input, .form-group select, .form-group textarea');
    formInputs.forEach(input => {
        input.addEventListener('blur', () => {
            validateField(input);
        });
        input.addEventListener('input', () => {
            const group = input.closest('.form-group');
            if (group && group.classList.contains('error')) {
                validateField(input);
            }
        });
        input.addEventListener('change', () => {
            const group = input.closest('.form-group');
            if (group && group.classList.contains('error')) {
                validateField(input);
            }
        });
    });

    function showStatusModal(isSuccess) {
        const title = isSuccess ? t.submitSuccessTitle : t.submitFailTitle;
        const desc = isSuccess ? t.submitSuccessDesc : t.submitFailDesc;
        
        let overlay = document.querySelector('.success-modal-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.className = 'success-modal-overlay';
            overlay.innerHTML = `
                <div class="success-modal-content">
                    <div class="success-modal-icon"></div>
                    <h3 class="success-modal-title"></h3>
                    <p class="success-modal-message"></p>
                    <button class="success-modal-btn"></button>
                </div>
            `;
            document.body.appendChild(overlay);
            
            overlay.querySelector('.success-modal-btn').addEventListener('click', () => {
                overlay.classList.remove('active');
            });
            
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) {
                    overlay.classList.remove('active');
                }
            });
        }
        
        const iconContainer = overlay.querySelector('.success-modal-icon');
        if (isSuccess) {
            iconContainer.style.color = 'var(--color-accent)';
            iconContainer.style.borderColor = 'var(--color-accent)';
            iconContainer.style.boxShadow = '0 0 20px rgba(13, 148, 136, 0.3)';
            iconContainer.innerHTML = `<svg class="lucide lucide-check" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
        } else {
            iconContainer.style.color = '#ef4444';
            iconContainer.style.borderColor = '#ef4444';
            iconContainer.style.boxShadow = '0 0 20px rgba(239, 68, 68, 0.3)';
            iconContainer.innerHTML = `<svg class="lucide lucide-alert-triangle" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>`;
        }
        
        overlay.querySelector('.success-modal-title').textContent = title;
        overlay.querySelector('.success-modal-message').textContent = desc;
        overlay.querySelector('.success-modal-btn').textContent = t.close;
        
        requestAnimationFrame(() => {
            overlay.classList.add('active');
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
            
            const isNameValid = validateField(name);
            const isPhoneValid = validateField(phone);
            const isEmailValid = validateField(email);
            
            if (!isNameValid || !isPhoneValid || !isEmailValid) {
                return;
            }

            // Disable button and show sending state
            const originalContent = rfpSubmitBtn.innerHTML;
            rfpSubmitBtn.innerHTML = `<span style="display:inline-flex;align-items:center;gap:8px;">${t.submitting}</span>`;
            rfpSubmitBtn.disabled = true;

            // Use FormData to allow file uploads
            const formData = new FormData(rfpForm);
            const actionUrl = rfpForm.getAttribute('action') || "https://formsubmit.co/jojo.li888@msa.hinet.net";

            fetch(actionUrl, {
                method: "POST",
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    showStatusModal(true);
                    
                    rfpForm.reset();
                    // Reset option cards selection
                    document.querySelectorAll('.rfp-option-card').forEach(c => c.classList.remove('selected'));
                    // Go back to step 1
                    rfpCurrentStep = 1;
                    updateRFPWizard();
                    
                    rfpSubmitBtn.innerHTML = originalContent;
                    rfpSubmitBtn.disabled = false;
                    if (typeof lucide !== 'undefined') {
                        lucide.createIcons();
                    }
                } else {
                    throw new Error("Form submission failed");
                }
            })
            .catch(error => {
                console.error(error);
                showStatusModal(false);
                rfpSubmitBtn.innerHTML = originalContent;
                rfpSubmitBtn.disabled = false;
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
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
            
            const isNameValid = validateField(name);
            const isPhoneValid = validateField(phone);
            const isEmailValid = validateField(email);
            
            if (!isNameValid || !isPhoneValid || !isEmailValid) {
                return;
            }

            const originalContent = generalSubmitBtn.innerHTML;
            generalSubmitBtn.innerHTML = `<span style="display:inline-flex;align-items:center;gap:8px;">${t.submitting}</span>`;
            generalSubmitBtn.disabled = true;

            const formData = new FormData(generalForm);
            const actionUrl = generalForm.getAttribute('action') || "https://formsubmit.co/jojo.li888@msa.hinet.net";

            fetch(actionUrl, {
                method: "POST",
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    showStatusModal(true);
                    
                    generalForm.reset();
                    generalSubmitBtn.innerHTML = originalContent;
                    generalSubmitBtn.disabled = false;
                    if (typeof lucide !== 'undefined') {
                        lucide.createIcons();
                    }
                } else {
                    throw new Error("Form submission failed");
                }
            })
            .catch(error => {
                console.error(error);
                showStatusModal(false);
                generalSubmitBtn.innerHTML = originalContent;
                generalSubmitBtn.disabled = false;
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            });
        });
    }
});
