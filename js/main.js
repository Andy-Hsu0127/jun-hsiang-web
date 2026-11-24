

/* ============================================================
   Jun-Hsiang RFQ Attribution Engine v1.0
   ============================================================ */
const ATTR_KEY = 'jh_rfq_attribution_v1';
const ATTR_VERSION = 'v1';

function getClusterFromPath(path) {
    const p = path.toLowerCase();
    if (p.includes('overmolding') || p.includes('vibration') || p.includes('bonding')) return 'overmolding';
    if (p.includes('lsr') || p.includes('liquid') || p.includes('service.html')) return 'lsr_injection';
    if (p.includes('oring') || p.includes('seal') || p.includes('waterproof') || p.includes('viton')) return 'seals_waterproof';
    if (p.includes('self-lubricating')) return 'self_lubricating';
    if (p.includes('conductive-keypad') || p.includes('keypad')) return 'conductive_keypad';
    if (p.includes('medical')) return 'medical_silicone';
    if (p.includes('food-grade')) return 'food_grade_silicone';
    if (p.includes('products_list') || p.includes('products')) return 'products_catalog';
    return 'general_factory';
}

function getArticleSlugFromPath(path) {
    const match = path.match(/knowledge-([a-zA-Z0-9_-]+)\.html/);
    return match ? match[1] : '';
}

function getTrafficSource(referrer) {
    if (!referrer) return 'direct';
    const ref = referrer.toLowerCase();
    if (ref.includes('google.')) return 'organic_google';
    if (ref.includes('bing.')) return 'organic_bing';
    if (ref.includes('yahoo.')) return 'organic_yahoo';
    if (ref.includes('baidu.')) return 'organic_baidu';
    if (ref.includes('linkedin.')) return 'social_linkedin';
    if (ref.includes('facebook.')) return 'social_facebook';
    try {
        const host = new URL(referrer).hostname;
        if (host && !host.includes('jun-hsiang.com.tw') && host !== window.location.hostname) {
            return 'referral_' + host.replace(/^www\./, '');
        }
    } catch (e) {}
    return 'internal_navigation';
}

function initAttribution() {
    const currentPath = window.location.pathname;
    const currentSlug = getArticleSlugFromPath(currentPath);
    const currentCluster = getClusterFromPath(currentPath);
    const urlParams = new URLSearchParams(window.location.search);
    
    let attr = null;
    try {
        const stored = sessionStorage.getItem(ATTR_KEY);
        if (stored) attr = JSON.parse(stored);
    } catch (e) {}
    
    const now = Date.now();
    
    if (!attr) {
        const referrer = document.referrer || '';
        const utmSrc = urlParams.get('utm_source') || '';
        const utmMed = urlParams.get('utm_medium') || '';
        const utmCamp = urlParams.get('utm_campaign') || '';
        const initialSource = utmSrc
            ? `utm:${utmSrc}/${utmMed || '-'}/${utmCamp || '-'}`
            : getTrafficSource(referrer);
        
        attr = {
            version: ATTR_VERSION,
            session_id: 'sess_' + Math.random().toString(36).substring(2, 9) + '_' + Math.floor(now / 1000),
            session_start_time: now,
            first_page: currentPath,
            first_source: initialSource,
            referrer: referrer,
            utm_source: utmSrc,
            utm_medium: utmMed,
            utm_campaign: utmCamp,
            first_content_touch: currentSlug || '',
            last_content_touch: currentSlug || '',
            source_cluster: currentCluster,
            journey: [currentPath]
        };
    } else {
        if (currentSlug) {
            if (!attr.first_content_touch) attr.first_content_touch = currentSlug;
            attr.last_content_touch = currentSlug;
            attr.source_cluster = currentCluster;
        }
        if (attr.journey && !attr.journey.includes(currentPath)) {
            attr.journey.push(currentPath);
        }
    }
    
    try {
        sessionStorage.setItem(ATTR_KEY, JSON.stringify(attr));
    } catch (e) {}
    
    return attr;
}

function getAttributionPayload() {
    let attr = initAttribution();
    const durationSec = Math.round((Date.now() - (attr.session_start_time || Date.now())) / 1000);
    
    let formattedJourney = '';
    if (attr.journey && attr.journey.length > 0) {
        if (attr.journey.length <= 5) {
            formattedJourney = attr.journey.join(' -> ');
        } else {
            const first = attr.journey[0];
            const recent = attr.journey.slice(-4);
            formattedJourney = `${first} -> ...[略過 ${attr.journey.length - 5} 頁] -> ${recent.join(' -> ')}`;
        }
    } else {
        formattedJourney = window.location.pathname;
    }
    
    return {
        rfq_first_page: attr.first_page || window.location.pathname,
        rfq_first_source: attr.first_source || 'direct',
        rfq_first_content: attr.first_content_touch || '(無)',
        rfq_last_content: attr.last_content_touch || '(無)',
        rfq_source_cluster: attr.source_cluster || 'general_factory',
        rfq_conversion_page: window.location.pathname,
        rfq_referrer: attr.referrer || '(direct)',
        rfq_utm_source: attr.utm_source || '(none)',
        rfq_utm_medium: attr.utm_medium || '(none)',
        rfq_utm_campaign: attr.utm_campaign || '(none)',
        rfq_session_id: attr.session_id || '',
        rfq_session_duration_sec: durationSec,
        rfq_journey_path: formattedJourney,
        rfq_attribution_version: attr.version || ATTR_VERSION
    };
}

function populateFormFields() {
    const payload = getAttributionPayload();
    const forms = document.querySelectorAll('#contact-form, #general-contact-form');
    forms.forEach(form => {
        if (!form.querySelector('input[name="_honey"]')) {
            const honey = document.createElement('input');
            honey.type = 'text';
            honey.name = '_honey';
            honey.style.display = 'none';
            honey.tabIndex = -1;
            honey.autocomplete = 'off';
            form.appendChild(honey);
        }
        Object.keys(payload).forEach(key => {
            let input = form.querySelector(`input[name="${key}"]`);
            if (!input) {
                input = document.createElement('input');
                input.type = 'hidden';
                input.name = key;
                form.appendChild(input);
            }
            input.value = payload[key];
        });
    });
}

function trackB2BConversion(actionType, label) {
    try {
        const payload = getAttributionPayload();
        const path = window.location.pathname || '';
        const lang = path.includes('/en/') ? 'en' : (path.includes('/ja/') ? 'ja' : 'zh-TW');
        const eventData = {
            event: 'b2b_conversion_action',
            action_type: actionType,
            action_label: label || '',
            page_lang: lang,
            article_slug: getArticleSlugFromPath(path) || 'non_article',
            utm_source: payload.rfq_utm_source,
            first_source: payload.rfq_first_source
        };
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push(eventData);
        if (typeof window.gtag === 'function') {
            window.gtag('event', actionType, {
                event_category: 'B2B_Conversion',
                event_label: label || eventData.article_slug,
                page_lang: lang,
                utm_source: payload.rfq_utm_source
            });
        }
    } catch (e) {}
}

window.JH_Attribution = {
    getPayload: getAttributionPayload,
    populateForms: populateFormFields,
    trackConversion: trackB2BConversion
};

document.addEventListener('DOMContentLoaded', () => {
    populateFormFields();

    document.addEventListener('click', (e) => {
        const copyBtn = e.target.closest('[data-copy-email]');
        if (!copyBtn) return;
        e.preventDefault();
        const emailToCopy = copyBtn.getAttribute('data-copy-email') || 'andy_hsu@jun-hsiang.com.tw';
        const origHtml = copyBtn.innerHTML;
        const copiedLabel = window.location.pathname.includes('/en/')
            ? '✅ Email Copied!'
            : (window.location.pathname.includes('/ja/') ? '✅ コピーしました！' : '✅ 已複製信箱！');
        const showCopied = () => {
            copyBtn.innerHTML = copiedLabel;
            setTimeout(() => { copyBtn.innerHTML = origHtml; }, 2500);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(emailToCopy).then(showCopied).catch(() => {
                const ta = document.createElement('textarea');
                ta.value = emailToCopy;
                document.body.appendChild(ta);
                ta.select();
                try { document.execCommand('copy'); } catch (err) {}
                document.body.removeChild(ta);
                showCopied();
            });
        } else {
            const ta = document.createElement('textarea');
            ta.value = emailToCopy;
            document.body.appendChild(ta);
            ta.select();
            try { document.execCommand('copy'); } catch (err) {}
            document.body.removeChild(ta);
            showCopied();
        }
    });

    function initFormThirdParties() {
        if (window.formThirdPartiesLoaded) return;
        window.formThirdPartiesLoaded = true;

        const s1 = document.createElement('script');
        s1.src = 'https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js';
        s1.onload = () => {
            if (typeof emailjs !== 'undefined') {
                emailjs.init({
                    publicKey: 'x4U1bJa_bowbuMl3r',
                    limitRate: {
                        id: 'jun-hsiang-app',
                        throttle: 30000,
                    }
                });
            }
        };
        document.body.appendChild(s1);

        const s2 = document.createElement('script');
        s2.src = 'https://www.google.com/recaptcha/api.js';
        s2.async = true;
        s2.defer = true;
        document.body.appendChild(s2);
    }

    const contactSection = document.getElementById('contact') || document.getElementById('rfq-section') || document.getElementById('general-contact-form');
    if (contactSection) {
        const contactObserver = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                initFormThirdParties();
                const mapIframe = document.querySelector('.map-container iframe[data-src]');
                if (mapIframe) mapIframe.src = mapIframe.dataset.src;
                contactObserver.disconnect();
            }
        }, { rootMargin: '200px' });
        contactObserver.observe(contactSection);
    } else {
        setTimeout(initFormThirdParties, 4000);
    }

    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    const isMobile = window.matchMedia('(max-width: 768px)').matches;
    const hero = document.querySelector('.hero');
    if (hero) hero.classList.add('loaded');

    if (window.initHeroParticles && !isMobile) {
        if ('requestIdleCallback' in window) {
            requestIdleCallback(() => window.initHeroParticles('hero-canvas'));
        } else {
            setTimeout(() => window.initHeroParticles('hero-canvas'), 500);
        }
    }

    const navbar = document.getElementById('navbar');
    let lastScrollY = 0;
    let ticking = false;

    function updateNavbar() {
        const scrollY = window.scrollY;

        if (scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        if (!isMobile) {
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

    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobile-menu');

    if (hamburger && mobileMenu) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            mobileMenu.classList.toggle('active');
            document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
        });

        mobileMenu.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                mobileMenu.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }

    const slides = document.querySelectorAll('.hero-slide');
    const dotsContainer = document.getElementById('hero-dots');
    const prevBtn = document.getElementById('hero-prev');
    const nextBtn = document.getElementById('hero-next');
    let currentSlide = 0;
    let slideInterval;

    if (slides.length > 0 && dotsContainer && prevBtn && nextBtn) {

        slides.forEach((_, index) => {
            const dot = document.createElement('span');
            dot.classList.add('dot');
            if (index === 0) dot.classList.add('active');
            dot.dataset.slide = index;
            dot.addEventListener('click', () => goToSlide(index));
            dotsContainer.appendChild(dot);
        });

        const dots = document.querySelectorAll('.dot');

        function loadSlideImage(slide) {
            if (slide.dataset.bg && !slide.dataset.bgLoaded) {
                slide.dataset.bgLoaded = '1';
                const img = new Image();
                img.onload = () => { slide.style.backgroundImage = `url('${slide.dataset.bg}')`; };
                img.src = slide.dataset.bg;
            }
        }

        function goToSlide(index) {
            slides[currentSlide].classList.remove('active');
            dots[currentSlide].classList.remove('active');
            currentSlide = (index + slides.length) % slides.length;

            loadSlideImage(slides[currentSlide]);
            // Preload the next slide in sequence
            const nextIndex = (currentSlide + 1) % slides.length;
            loadSlideImage(slides[nextIndex]);

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
        // Preload only slide 2 image after page is idle (not all at once)
        if ('requestIdleCallback' in window) {
            requestIdleCallback(() => loadSlideImage(slides[1]), { timeout: 3000 });
        } else {
            setTimeout(() => loadSlideImage(slides[1]), 3000);
        }
    }

    const categoryItems = document.querySelectorAll('.category-item');
    const productCards = document.querySelectorAll('.product-card');

    categoryItems.forEach(item => {
        item.addEventListener('click', () => {
            categoryItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');

            const filter = item.dataset.filter;

            productCards.forEach(card => {
                if (filter === 'all' || card.dataset.category.includes(filter)) {
                    card.style.display = '';
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.9)';
                    requestAnimationFrame(() => {
                        card.style.transition = 'opacity 0.4s cubic-bezier(0.16, 1, 0.3, 1), transform 0.4s cubic-bezier(0.16, 1, 0.3, 1)';
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

    const urlParams = new URLSearchParams(window.location.search);
    const catParam = urlParams.get('category');
    if (catParam) {
        const targetItem = Array.from(categoryItems).find(item => item.dataset.filter === catParam);
        if (targetItem) {

            setTimeout(() => {
                targetItem.click();
            }, 100);
        }
    }

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

    const modal = document.getElementById('product-modal');
    const modalClose = document.getElementById('modal-close');
    const modalBackdrop = document.getElementById('modal-backdrop');

    function openModal(card) {
        if (!modal) return;

        document.getElementById('modal-title').textContent = card.dataset.title || '';
        document.getElementById('modal-title-small').textContent = card.dataset.title || '';
        document.getElementById('modal-category-text').textContent = card.dataset.type || '';
        document.getElementById('modal-desc').textContent = card.dataset.desc || '';
        document.getElementById('modal-img').src = card.dataset.img || '';

        modal.classList.add('show');
        document.body.style.overflow = 'hidden'; // prevent background scrolling

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

        document.querySelectorAll('.product-card').forEach(card => {
            card.addEventListener('click', () => openModal(card));

            let tiltRaf = null;
            card.addEventListener('mousemove', (e) => {
                if (tiltRaf) return;
                tiltRaf = requestAnimationFrame(() => {
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    card.style.setProperty('--mouse-x', `${x}px`);
                    card.style.setProperty('--mouse-y', `${y}px`);
                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;
                    const rotateX = (y - centerY) / 10;
                    const rotateY = (centerX - x) / 10;
                    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
                    tiltRaf = null;
                });
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
    }

    window.closeModal = closeModal;

    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        if (question) {
            question.addEventListener('click', () => {
                const isActive = item.classList.contains('active');

                faqItems.forEach(otherItem => {
                    otherItem.classList.remove('active');
                });

                if (!isActive) {
                    item.classList.add('active');
                }
            });
        }
    });

    const glowCards = document.querySelectorAll('.glow-card');
    glowCards.forEach(card => {
        let glowRaf = null;
        card.addEventListener('mousemove', (e) => {
            if (glowRaf) return;
            glowRaf = requestAnimationFrame(() => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
                glowRaf = null;
            });
        });
    });

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

            grid.querySelectorAll('.rfp-option-card').forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
        });
    });

    let rfpCurrentStep = 1;
    const rfpTotalSteps = 4;
    const rfpPrevBtn = document.getElementById('rfp-prev-btn');
    const rfpNextBtn = document.getElementById('rfp-next-btn');
    const rfpSubmitBtn = document.getElementById('rfp-submit-btn');
    const rfpProgressBar = document.getElementById('rfp-progress');
    const rfpStepDots = document.querySelectorAll('.rfp-step-dot');
    const rfpSteps = document.querySelectorAll('.rfp-step');

    function updateRFPWizard() {

        rfpSteps.forEach(step => {
            if (parseInt(step.dataset.step) === rfpCurrentStep) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });

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

        const progressPercent = ((rfpCurrentStep - 1) / (rfpTotalSteps - 1)) * 100;
        if (rfpProgressBar) {
            rfpProgressBar.style.width = `${25 + progressPercent * 0.75}%`; // start at 25%, end at 100%
        }

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
            captchaHint: '💡 請勾選上方「我不是機器人」安全驗證以立即送出（若無法顯示驗證框，再點一次送出按鈕即可直接傳送）。',
            attachFollowupDesc: '為確保您的工程圖檔（{file}）完整送達不被濾除，請點擊下方按鈕直接開啟信箱夾帶原檔寄出：',
            attachBtnText: '📎 開啟信箱夾帶原檔寄至 andy_hsu@jun-hsiang.com.tw',
            floatingRfq: '✉️ 傳圖詢價',
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
            submitFailDesc: 'Sorry, we are unable to process your request at this time. Please email us directly at andy_hsu@jun-hsiang.com.tw or try again later.',
            captchaHint: '💡 Please check the "I am not a robot" box above to send (or click Submit once more to send directly if the widget is blocked).',
            attachFollowupDesc: 'To ensure your CAD/drawing file ({file}) arrives intact without mail-server size/type filtering, please click below to attach and email it directly:',
            attachBtnText: '📎 Attach & Email File to andy_hsu@jun-hsiang.com.tw',
            floatingRfq: '✉️ Send CAD / RFQ',
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
            submitFailDesc: '申し訳ありませんが、現在リクエストを処理できません。andy_hsu@jun-hsiang.com.tw へ直接メールをお送りいただくか、時間をおいて再度お試しください。',
            captchaHint: '💡 上の「私はロボットではありません」にチェックを入れて送信してください（表示されない場合はもう一度送信ボタンを押してください）。',
            attachFollowupDesc: '図面ファイル（{file}）を確実にお受け取りするため、下のボタンからメールソフトを開き、原図ファイルを添付して直接ご送付ください：',
            attachBtnText: '📎 メールを開いて図面を添付送付 (andy_hsu@jun-hsiang.com.tw)',
            floatingRfq: '✉️ 図面見積り',
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


    const phoneInputs = document.querySelectorAll('#general-phone, #rfp-phone');
    phoneInputs.forEach(input => {
        input.addEventListener('input', () => {
            const cleaned = input.value.replace(/[^\d\s()+\-]/g, '');
            if (input.value !== cleaned) {
                input.value = cleaned;
            }
        });
    });

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

            validateField(input);
        });
    });

    function resetAllRecaptchas() {
        if (typeof grecaptcha === 'undefined') return;
        try {
            const widgets = document.querySelectorAll('.g-recaptcha');
            widgets.forEach((_, idx) => {
                try { grecaptcha.reset(idx); } catch (err) {}
            });
        } catch (err) {}
    }

    function sendViaEmailJS(templateParams) {
        return fetch("https://api.emailjs.com/api/v1.0/email/send", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                service_id: "service_941qf5m",
                template_id: "template_xd47fdq",
                user_id: "x4U1bJa_bowbuMl3r",
                template_params: templateParams
            })
        }).then(res => {
            if (!res.ok) throw new Error("EmailJS HTTP " + res.status);
            return res;
        });
    }

    function showStatusModal(isSuccess, attachmentInfo) {
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
                    <div class="success-modal-attach-box" style="display:none;margin-bottom:18px;padding:12px;background:rgba(13,148,136,0.1);border:1px solid rgba(13,148,136,0.35);border-radius:8px;">
                        <p class="success-modal-attach-desc" style="font-size:0.86rem;margin:0 0 10px 0;color:var(--color-text-secondary);"></p>
                        <a class="success-modal-attach-btn" href="#" style="display:inline-block;background:var(--color-accent);color:#fff;padding:8px 14px;border-radius:6px;font-size:0.85rem;font-weight:700;text-decoration:none;"></a>
                    </div>
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

        const attachBox = overlay.querySelector('.success-modal-attach-box');
        if (isSuccess && attachmentInfo && attachmentInfo.fileName) {
            const subj = encodeURIComponent(`[Jun-Hsiang CAD Attachment] ${attachmentInfo.company || attachmentInfo.name || 'RFQ'} - ${attachmentInfo.fileName}`);
            const body = encodeURIComponent(`Contact: ${attachmentInfo.name || ''}\nCompany: ${attachmentInfo.company || ''}\nEmail: ${attachmentInfo.email || ''}\nPhone: ${attachmentInfo.phone || ''}\nProduct/Process: ${attachmentInfo.product || ''}\nSelected File: ${attachmentInfo.fileName}\n\n(Please attach ${attachmentInfo.fileName} to this email and click Send.)`);
            attachBox.querySelector('.success-modal-attach-desc').textContent = t.attachFollowupDesc.replace('{file}', attachmentInfo.fileName);
            const btn = attachBox.querySelector('.success-modal-attach-btn');
            btn.textContent = t.attachBtnText;
            btn.href = `mailto:andy_hsu@jun-hsiang.com.tw?subject=${subj}&body=${body}`;
            attachBox.style.display = 'block';
        } else if (attachBox) {
            attachBox.style.display = 'none';
        }
        
        requestAnimationFrame(() => {
            overlay.classList.add('active');
        });
    }

    const rfpForm = document.getElementById('contact-form');
    if (rfpForm) {
        rfpForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const name = document.getElementById('rfp-name');
            const phone = document.getElementById('rfp-phone');
            const email = document.getElementById('rfp-email');
            
            const isNameValid = validateField(name);
            const isPhoneValid = validateField(phone);
            const isEmailValid = validateField(email);
            
            if (!isNameValid || !isPhoneValid || !isEmailValid) {
                return;
            }

            const honeyEl = rfpForm.querySelector('input[name="_honey"]');
            if (honeyEl && honeyEl.value) return;
            const captchaEl = rfpForm.querySelector('[name="g-recaptcha-response"]');
            const captchaToken = captchaEl ? captchaEl.value : "";

            const originalContent = rfpSubmitBtn.innerHTML;
            rfpSubmitBtn.innerHTML = `<span style="display:inline-flex;align-items:center;gap:8px;">${t.submitting}</span>`;
            rfpSubmitBtn.disabled = true;

            const fileInput = document.getElementById('rfp-file');
            const hasFile = fileInput && fileInput.files && fileInput.files.length > 0;
            const rfpAttachInfo = hasFile ? {
                fileName: fileInput.files[0].name,
                company: document.getElementById('rfp-company') ? document.getElementById('rfp-company').value : "",
                name: document.getElementById('rfp-name') ? document.getElementById('rfp-name').value : "",
                phone: document.getElementById('rfp-phone') ? document.getElementById('rfp-phone').value : "",
                email: document.getElementById('rfp-email') ? document.getElementById('rfp-email').value : "",
                product: document.getElementById('rfp-process') ? document.getElementById('rfp-process').value : ""
            } : null;

            let rfpLeadTracked = false;
            const handleRFPSuccess = (deliveryMethod) => {
                if (!rfpLeadTracked) {
                    rfpLeadTracked = true;
                    if (typeof window.JH_TrackLeadSuccess === 'function') {
                        window.JH_TrackLeadSuccess('contact-form', deliveryMethod || 'emailjs');
                    }
                }
                showStatusModal(true, rfpAttachInfo);
                rfpForm.reset();
                delete rfpForm.dataset.captchaWarned;
                document.querySelectorAll('.rfp-option-card').forEach(c => c.classList.remove('selected'));
                rfpCurrentStep = 1;
                updateRFPWizard();
                rfpSubmitBtn.innerHTML = originalContent;
                rfpSubmitBtn.disabled = false;
                resetAllRecaptchas();
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            };

            const handleRFPError = (error) => {
                console.error(error);
                showStatusModal(false);
                rfpSubmitBtn.innerHTML = originalContent;
                rfpSubmitBtn.disabled = false;
                resetAllRecaptchas();
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            };

            const fileNote = hasFile
                ? `\n📎 客戶已夾帶圖檔: ${fileInput.files[0].name} (${Math.max(1, Math.round(fileInput.files[0].size / 1024))} KB)`
                : '';

            if (hasFile) {
                const formData = new FormData(rfpForm);
                const actionUrl = rfpForm.getAttribute('action') || "https://formsubmit.co/jojo.li888@msa.hinet.net";
                fetch(actionUrl, {
                    method: "POST",
                    mode: "no-cors",
                    body: formData
                }).catch(err => console.warn("Background attachment upload notice:", err));
            }

            const appVal = document.getElementById('rfp-application') ? document.getElementById('rfp-application').value || "未填寫" : "未填寫";
            const procVal = document.getElementById('rfp-process') ? document.getElementById('rfp-process').value || "未填寫" : "未填寫";
            const qtyVal = document.getElementById('rfp-quantity') ? document.getElementById('rfp-quantity').value || "未填寫" : "未填寫";
            const hardVal = document.getElementById('rfp-hardness') ? document.getElementById('rfp-hardness').value || "未填寫" : "未填寫";
            const tempVal = document.getElementById('rfp-temp') ? document.getElementById('rfp-temp').value || "未填寫" : "未填寫";
            const msgVal = document.getElementById('rfp-message') ? document.getElementById('rfp-message').value || "無" : "無";

            const attr = window.JH_Attribution ? window.JH_Attribution.getPayload() : {};
            const attrText = `\n\n【SEO 商業歸因 (v1)】\n首次進站: ${attr.rfq_first_page || '直接'} (${attr.rfq_first_source || 'direct'})\n首次內容: ${attr.rfq_first_content || '(無)'}\n最後內容: ${attr.rfq_last_content || '(無)'} (叢集: ${attr.rfq_source_cluster || 'general'})\n轉換頁面: ${attr.rfq_conversion_page || window.location.pathname}\n停留秒數: ${attr.rfq_session_duration_sec || 0}s\n瀏覽旅程: ${attr.rfq_journey_path || '直接'}`;

            const templateParams = {
                company: document.getElementById('rfp-company') ? document.getElementById('rfp-company').value : "",
                name: document.getElementById('rfp-name') ? document.getElementById('rfp-name').value : "",
                phone: document.getElementById('rfp-phone') ? document.getElementById('rfp-phone').value : "",
                email: document.getElementById('rfp-email') ? document.getElementById('rfp-email').value : "",
                product: `應用領域: ${appVal} | 加工製程: ${procVal}`,
                message: `預估年產量: ${qtyVal}\n硬度要求: ${hardVal}\n使用溫度: ${tempVal}\n其他補充需求: ${msgVal}${fileNote}${attrText}`,
                'g-recaptcha-response': captchaToken
            };

            const sendRFPFormSubmitFallback = (error) => {
                fetch("https://formsubmit.co/ajax/jojo.li888@msa.hinet.net", {
                    method: "POST",
                    headers: { "Content-Type": "application/json", "Accept": "application/json" },
                    body: JSON.stringify({
                        "公司名稱": templateParams.company,
                        "聯絡姓名": templateParams.name,
                        "聯絡電話": templateParams.phone,
                        "E-mail": templateParams.email,
                        "需求細節": templateParams.product,
                        "補充說明": templateParams.message,
                        "首次進站": attr.rfq_first_page || "直接",
                        "流量來源": attr.rfq_first_source || "direct",
                        "首次內容": attr.rfq_first_content || "無",
                        "最後內容": attr.rfq_last_content || "無",
                        "所屬叢集": attr.rfq_source_cluster || "general",
                        "瀏覽旅程": attr.rfq_journey_path || "無",
                        "_cc": "andy_hsu@jun-hsiang.com.tw",
                        "_subject": "【鈞翔實業官網】專案需求聯絡 (含歸因資訊)"
                    })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success === "true" || data.success === true) {
                        handleRFPSuccess('formsubmit');
                    } else {
                        handleRFPError(error);
                    }
                })
                .catch(() => handleRFPError(error));
            };

            sendViaEmailJS(templateParams)
            .then(() => {
                handleRFPSuccess('emailjs');
            })
            .catch(error => {
                console.warn("EmailJS failed, trying FormSubmit fallback...", error);
                sendRFPFormSubmitFallback(error);
            });
        });
    }

    const materialHelper = document.getElementById('material-results');
    if (materialHelper) {
        const checkboxes = document.querySelectorAll('.material-checkbox-input');
        const cards = document.querySelectorAll('.material-result-card');
        const emptyState = document.getElementById('material-helper-empty');

        function filterMaterials() {

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

                    card.classList.remove('hidden');
                    visibleCount++;
                } else {

                    const isMatch = activeProps.some(prop => cardTags.includes(prop));
                    if (isMatch) {
                        card.classList.remove('hidden');
                        visibleCount++;
                    } else {
                        card.classList.add('hidden');
                    }
                }
            });

            if (visibleCount === 0 && emptyState) {
                emptyState.classList.remove('hidden');
            } else if (emptyState) {
                emptyState.classList.add('hidden');
            }
        }

        checkboxes.forEach(cb => {
            cb.addEventListener('change', filterMaterials);
        });

        filterMaterials();
    }

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
                const hiddenRecaptcha = targetContent.querySelector('.g-recaptcha');
                if (hiddenRecaptcha && hiddenRecaptcha.innerHTML.trim() === '' && typeof grecaptcha !== 'undefined' && typeof grecaptcha.render === 'function') {
                    try {
                        grecaptcha.render(hiddenRecaptcha, { sitekey: hiddenRecaptcha.getAttribute('data-sitekey') });
                    } catch (err) {}
                }
            }
        });
    });

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

            const honeyEl = generalForm.querySelector('input[name="_honey"]');
            if (honeyEl && honeyEl.value) return;
            const captchaEl = generalForm.querySelector('[name="g-recaptcha-response"]');
            const captchaToken = captchaEl ? captchaEl.value : "";

            const originalContent = generalSubmitBtn.innerHTML;
            generalSubmitBtn.innerHTML = `<span style="display:inline-flex;align-items:center;gap:8px;">${t.submitting}</span>`;
            generalSubmitBtn.disabled = true;

            const genFileInput = document.getElementById('general-file');
            const hasGenFile = genFileInput && genFileInput.files && genFileInput.files.length > 0;
            const genAttachInfo = hasGenFile ? {
                fileName: genFileInput.files[0].name,
                company: document.getElementById('general-company') ? document.getElementById('general-company').value : "",
                name: document.getElementById('general-name') ? document.getElementById('general-name').value : "",
                phone: document.getElementById('general-phone') ? document.getElementById('general-phone').value : "",
                email: document.getElementById('general-email') ? document.getElementById('general-email').value : "",
                product: document.getElementById('general-product-need') ? document.getElementById('general-product-need').value : ""
            } : null;
            const genFileNote = hasGenFile
                ? `\n📎 客戶已夾帶圖檔: ${genFileInput.files[0].name} (${Math.max(1, Math.round(genFileInput.files[0].size / 1024))} KB)`
                : '';

            if (hasGenFile) {
                const formData = new FormData(generalForm);
                const actionUrl = generalForm.getAttribute('action') || "https://formsubmit.co/jojo.li888@msa.hinet.net";
                fetch(actionUrl, {
                    method: "POST",
                    mode: "no-cors",
                    body: formData
                }).catch(err => console.warn("Background attachment upload notice:", err));
            }

            const attr = window.JH_Attribution ? window.JH_Attribution.getPayload() : {};
            const attrText = `\n\n【SEO 商業歸因 (v1)】\n首次進站: ${attr.rfq_first_page || '直接'} (${attr.rfq_first_source || 'direct'})\n首次內容: ${attr.rfq_first_content || '(無)'}\n最後內容: ${attr.rfq_last_content || '(無)'} (叢集: ${attr.rfq_source_cluster || 'general'})\n轉換頁面: ${attr.rfq_conversion_page || window.location.pathname}\n停留秒數: ${attr.rfq_session_duration_sec || 0}s\n瀏覽旅程: ${attr.rfq_journey_path || '直接'}`;

            const templateParams = {
                company: document.getElementById('general-company') ? document.getElementById('general-company').value : "",
                name: document.getElementById('general-name') ? document.getElementById('general-name').value : "",
                phone: document.getElementById('general-phone') ? document.getElementById('general-phone').value : "",
                email: document.getElementById('general-email') ? document.getElementById('general-email').value : "",
                product: document.getElementById('general-product-need') ? document.getElementById('general-product-need').value : "",
                message: (document.getElementById('general-message') ? document.getElementById('general-message').value : "") + genFileNote + attrText,
                'g-recaptcha-response': captchaToken
            };

            let genLeadTracked = false;
            const fireGeneralLeadSuccess = (deliveryMethod) => {
                if (!genLeadTracked) {
                    genLeadTracked = true;
                    if (typeof window.JH_TrackLeadSuccess === 'function') {
                        window.JH_TrackLeadSuccess('general-contact-form', deliveryMethod || 'emailjs');
                    }
                }
            };

            const sendGenFormSubmitFallback = () => {
                fetch("https://formsubmit.co/ajax/jojo.li888@msa.hinet.net", {
                    method: "POST",
                    headers: { "Content-Type": "application/json", "Accept": "application/json" },
                    body: JSON.stringify({
                        "公司名稱": templateParams.company,
                        "聯絡姓名": templateParams.name,
                        "聯絡電話": templateParams.phone,
                        "E-mail": templateParams.email,
                        "需求產品": templateParams.product,
                        "留言內容": templateParams.message,
                        "首次進站": attr.rfq_first_page || "直接",
                        "流量來源": attr.rfq_first_source || "direct",
                        "首次內容": attr.rfq_first_content || "無",
                        "最後內容": attr.rfq_last_content || "無",
                        "所屬叢集": attr.rfq_source_cluster || "general",
                        "瀏覽旅程": attr.rfq_journey_path || "無",
                        "_cc": "andy_hsu@jun-hsiang.com.tw",
                        "_subject": "【鈞翔實業官網】一般聯絡詢問 (含歸因資訊)"
                    })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success === "true" || data.success === true) {
                        fireGeneralLeadSuccess('formsubmit');
                        showStatusModal(true, genAttachInfo);
                        generalForm.reset();
                        delete generalForm.dataset.captchaWarned;
                    } else {
                        showStatusModal(false);
                    }
                })
                .catch(() => {
                    showStatusModal(false);
                })
                .finally(() => {
                    generalSubmitBtn.innerHTML = originalContent;
                    generalSubmitBtn.disabled = false;
                    resetAllRecaptchas();
                    if (typeof lucide !== 'undefined') lucide.createIcons();
                });
            };

            sendViaEmailJS(templateParams)
            .then(() => {
                fireGeneralLeadSuccess('emailjs');
                showStatusModal(true, genAttachInfo);
                generalForm.reset();
                delete generalForm.dataset.captchaWarned;
                generalSubmitBtn.innerHTML = originalContent;
                generalSubmitBtn.disabled = false;
                resetAllRecaptchas();
                if (typeof lucide !== 'undefined') lucide.createIcons();
            })
            .catch(error => {
                console.warn("EmailJS failed, trying FormSubmit fallback...", error);
                sendGenFormSubmitFallback();
            });
        });
    }

    const lazyVideo = document.getElementById('intro-video');
    if (lazyVideo) {
        const videoObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const video = entry.target;
                    video.src = video.dataset.src;
                    video.load();
                    videoObserver.unobserve(video);
                }
            });
        }, { threshold: 0.1 });
        videoObserver.observe(lazyVideo);

        lazyVideo.addEventListener('ended', () => {
            const productsSection = document.getElementById('products');
            if (productsSection) {
                productsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    }

    // Language Dropdown Click & Touch Toggle
    const langSelectors = document.querySelectorAll('.lang-selector');
    langSelectors.forEach(selector => {
        const btn = selector.querySelector('.lang-selector-btn');
        if (btn) {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const isOpen = selector.classList.contains('is-open');
                // Close all other open selectors
                langSelectors.forEach(s => s.classList.remove('is-open'));
                if (!isOpen) {
                    selector.classList.add('is-open');
                }
            });
        }
    });

    document.addEventListener('click', (e) => {
        if (!e.target.closest('.lang-selector')) {
            langSelectors.forEach(s => s.classList.remove('is-open'));
        }
    });

    const rfqTarget = document.getElementById('rfq-section');
    if (rfqTarget) {
        const floatBtn = document.createElement('a');
        floatBtn.href = '#rfq-section';
        floatBtn.textContent = t.floatingRfq;
        floatBtn.style.cssText = 'position:fixed;right:20px;bottom:84px;z-index:990;background:var(--color-accent,#0D9488);color:#fff;padding:10px 16px;border-radius:999px;font-size:0.86rem;font-weight:700;text-decoration:none;box-shadow:0 8px 24px rgba(13,148,136,0.35);opacity:0;pointer-events:none;transition:opacity 0.25s ease,transform 0.25s ease;transform:translateY(8px);';
        floatBtn.addEventListener('click', (e) => {
            e.preventDefault();
            rfqTarget.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
        document.body.appendChild(floatBtn);
        let floatTick = false;
        window.addEventListener('scroll', () => {
            if (floatTick) return;
            floatTick = true;
            requestAnimationFrame(() => {
                const show = window.scrollY > 400;
                floatBtn.style.opacity = show ? '1' : '0';
                floatBtn.style.pointerEvents = show ? 'auto' : 'none';
                floatBtn.style.transform = show ? 'translateY(0)' : 'translateY(8px)';
                floatTick = false;
            });
        }, { passive: true });
    }

    // Taiwan-only Official LINE Floating Button (@682wvagy) - strictly excluded from /en/ and /ja/
    const isZhOnlyPage = !window.location.pathname.includes('/en/') && !window.location.pathname.includes('/ja/') && (document.documentElement.lang || '').toLowerCase().startsWith('zh');
    if (isZhOnlyPage && !document.getElementById('tw-line-float-btn')) {
        const lineBtn = document.createElement('a');
        lineBtn.id = 'tw-line-float-btn';
        lineBtn.href = 'https://line.me/R/ti/p/@682wvagy';
        lineBtn.target = '_blank';
        lineBtn.rel = 'noopener noreferrer';
        lineBtn.setAttribute('aria-label', '加入鈞翔實業官方 LINE 傳圖估價 (@682wvagy)');
        lineBtn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19.365 9.863c.349 0 .63.285.63.631 0 .345-.281.63-.63.63H17.61v1.125h1.755c.349 0 .63.283.63.63 0 .344-.281.629-.63.629h-2.386c-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63h2.386c.346 0 .627.285.627.63 0 .349-.281.63-.63.63H17.61v1.125h1.755zm-3.855 3.016c0 .27-.174.51-.432.596-.064.021-.133.031-.199.031-.211 0-.391-.09-.51-.25l-2.443-3.317v2.94c0 .344-.279.629-.631.629-.346 0-.626-.285-.626-.629V8.108c0-.27.173-.51.43-.595.06-.023.136-.033.194-.033.195 0 .375.104.495.254l2.462 3.33V8.108c0-.345.282-.63.63-.63.345 0 .63.285.63.63v4.771zm-5.741 0c0 .344-.282.629-.631.629-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63.346 0 .628.285.628.63v4.771zm-2.466.629H4.917c-.345 0-.63-.285-.63-.629V8.108c0-.345.285-.63.63-.63.348 0 .63.285.63.63v4.141h1.756c.348 0 .629.283.629.63 0 .344-.282.629-.629.629M24 10.314C24 4.943 18.615.572 12 .572S0 4.943 0 10.314c0 4.811 4.27 8.842 10.035 9.608.391.082.923.258 1.058.59.12.301.079.766.038 1.08l-.164 1.02c-.045.301-.24 1.186 1.049.645 1.291-.539 6.916-4.078 9.436-6.975C23.176 14.393 24 12.458 24 10.314"/></svg><span>LINE 傳圖估價</span>';
        lineBtn.style.cssText = 'position:fixed;left:20px;bottom:24px;z-index:991;display:inline-flex;align-items:center;gap:8px;background:#06C755;color:#fff;padding:11px 16px;border-radius:999px;font-size:0.88rem;font-weight:700;text-decoration:none;box-shadow:0 8px 24px rgba(6,199,85,0.38);transition:transform 0.2s ease;';
        document.body.appendChild(lineBtn);
    }

    // Global 3-Language Site Search Modal (Keyword + 2-Layer Dropdown: Category x Industry)
    (function initSiteSearch() {
        const path = window.location.pathname || '';
        const sLang = path.includes('/en/') ? 'en' : path.includes('/ja/') ? 'ja' : 'zh';
        const ui = {
            zh: {
                btnLabel: '搜尋',
                btnAria: '開啟全站搜尋與分類篩選',
                title: '全站搜尋與分類篩選',
                placeholder: '輸入關鍵字（如 LSR、硬度、FDA、包鐵、防水栓、Viton）...',
                catLabel: '內容類別',
                cats: [
                    ['all', '全部類別'],
                    ['process', '製程與開模代工'],
                    ['product', '產品與實績項目'],
                    ['material', '材料規格與異常排查']
                ],
                indLabel: '應用產業',
                inds: [
                    ['all', '全部應用產業'],
                    ['auto', '車載與線束防水'],
                    ['med_food', '醫療與食品接觸'],
                    ['semi_ai', '半導體與 AI 伺服器'],
                    ['industrial', '工業機械與防振'],
                    ['uav_3c', '無人機與 3C 電子']
                ],
                catTag: { process: '製程代工', product: '產品實績', material: '材料規格' },
                count: (n) => `共 ${n} 筆符合項目（點擊下方項目即可前往頁面）`,
                goLabel: '前往 ➔',
                loading: '載入檢索資料中...',
                emptyTitle: '找不到完全符合的規格或文章',
                emptyDesc: '歡迎直接傳送 2D/3D 圖檔或需求，由新北新莊工程團隊 1～2 個工作天免費評估（支援少量試產打樣）。',
                rfqBtn: '✉️ 線上傳圖詢價',
                lineBtn: '💬 加官方 LINE 傳圖（@682wvagy）'
            },
            en: {
                btnLabel: 'Search',
                btnAria: 'Open site search and category filter',
                title: 'Site Search & Category Filter',
                placeholder: 'Search keywords (LSR, Shore A, FDA, overmolding, Viton, seals)...',
                catLabel: 'Category',
                cats: [
                    ['all', 'All Categories'],
                    ['process', 'Molding & Processes'],
                    ['product', 'Custom Products & Cases'],
                    ['material', 'Materials & Compliance']
                ],
                indLabel: 'Industry',
                inds: [
                    ['all', 'All Industries'],
                    ['auto', 'Automotive & Wire Harness'],
                    ['med_food', 'Medical & Food-Grade'],
                    ['semi_ai', 'Semiconductor & AI Server'],
                    ['industrial', 'Industrial Machinery'],
                    ['uav_3c', 'UAV Drones & Electronics']
                ],
                catTag: { process: 'Process', product: 'Product', material: 'Material' },
                count: (n) => `${n} matching pages (click any item below to open)`,
                goLabel: 'Open →',
                loading: 'Loading search index...',
                emptyTitle: 'No exact match found for your specification',
                emptyDesc: 'Send your 2D/3D CAD drawings for a free engineering review and quotation (Mutual NDA ready).',
                rfqBtn: '✉️ Request Quote with CAD',
                lineBtn: ''
            },
            ja: {
                btnLabel: '検索',
                btnAria: 'サイト内検索・カテゴリ絞り込みを開く',
                title: 'サイト内検索・カテゴリ絞り込み',
                placeholder: 'キーワード入力（LSR、硬度、FDA、インサート、Viton、シール）...',
                catLabel: 'カテゴリ',
                cats: [
                    ['all', 'すべてのカテゴリ'],
                    ['process', '成形プロセス・受託製造'],
                    ['product', '製品事例・ラインナップ'],
                    ['material', '材料仕様・規格・対策']
                ],
                indLabel: '産業分野',
                inds: [
                    ['all', 'すべての産業分野'],
                    ['auto', '車載・ワイヤーハーネス'],
                    ['med_food', '医療・食品グレード'],
                    ['semi_ai', '半導体・AIサーバー'],
                    ['industrial', '産業機械・防振'],
                    ['uav_3c', 'ドローン・電子機器']
                ],
                catTag: { process: '成形プロセス', product: '製品事例', material: '材料・規格' },
                count: (n) => `${n} 件の結果（下の項目をクリックして移動）`,
                goLabel: '開く →',
                loading: '検索データを読み込み中...',
                emptyTitle: '該当する仕様・記事が見つかりませんでした',
                emptyDesc: '2D/3D図面をお送りいただければ、台湾自社工場のエンジニアが無料でお見積り・技術評価いたします。',
                rfqBtn: '✉️ 図面でお問い合わせ',
                lineBtn: ''
            }
        }[sLang];

        const ham = document.getElementById('hamburger');
        if (!ham || !ham.parentElement || document.getElementById('site-search-trigger')) return;

        const trigger = document.createElement('button');
        trigger.id = 'site-search-trigger';
        trigger.type = 'button';
        trigger.setAttribute('aria-label', ui.btnAria);
        trigger.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.3-4.3"></path></svg><span>' + ui.btnLabel + '</span>';
        if (!document.getElementById('site-search-nav-style')) {
            const st = document.createElement('style');
            st.id = 'site-search-nav-style';
            st.textContent = '#nav-links{margin-left:auto;margin-right:12px;}#site-search-trigger{display:inline-flex;align-items:center;gap:6px;margin-left:0;margin-right:0;padding:6px 12px;border-radius:999px;border:1px solid rgba(212,168,67,0.45);background:rgba(15,23,42,0.75);color:#F8FAFC;font-size:0.84rem;font-weight:600;cursor:pointer;white-space:nowrap;flex-shrink:0;transition:border-color 0.2s ease,transform 0.2s ease;}#site-search-trigger:hover{border-color:#D4A843;}.site-search-item{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 14px;margin-bottom:8px;border-radius:9px;border:1px solid rgba(148,163,184,0.2);background:rgba(30,41,59,0.62);text-decoration:none;cursor:pointer;transition:border-color 0.18s ease,background-color 0.18s ease;}.site-search-item:hover{border-color:#D4A843;background:rgba(30,41,59,0.95);}@media(max-width:968px){#site-search-trigger{margin-left:auto;margin-right:12px;}}';
            document.head.appendChild(st);
        }
        ham.parentElement.insertBefore(trigger, ham);

        let modal = null;
        let indexCache = null;

        function escapeHtml(str) {
            return String(str || '').replace(/[&<>"']/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]));
        }

        function ensureModal() {
            if (modal) return modal;
            modal = document.createElement('div');
            modal.id = 'site-search-modal';
            modal.setAttribute('role', 'dialog');
            modal.setAttribute('aria-modal', 'true');
            modal.setAttribute('aria-label', ui.title);
            modal.style.cssText = 'display:none;position:fixed;inset:0;z-index:9999;background:rgba(4,9,20,0.78);backdrop-filter:blur(6px);padding:clamp(12px,4vh,48px) 14px;overflow-y:auto;';
            const catOpts = ui.cats.map(([v, l]) => `<option value="${v}">${escapeHtml(l)}</option>`).join('');
            const indOpts = ui.inds.map(([v, l]) => `<option value="${v}">${escapeHtml(l)}</option>`).join('');
            modal.innerHTML = `
                <div style="max-width:740px;margin:0 auto;background:#0F172A;border:1px solid rgba(212,168,67,0.38);border-radius:14px;box-shadow:0 24px 64px rgba(0,0,0,0.55);overflow:hidden;">
                    <div style="display:flex;align-items:center;justify-content:space-between;padding:14px 18px;border-bottom:1px solid rgba(148,163,184,0.18);">
                        <strong style="color:#F8FAFC;font-size:1rem;display:inline-flex;align-items:center;gap:8px;">🔍 ${escapeHtml(ui.title)}</strong>
                        <button type="button" id="site-search-close" aria-label="Close" style="background:transparent;border:none;color:#94A3B8;font-size:1.35rem;line-height:1;cursor:pointer;padding:4px 8px;">✕</button>
                    </div>
                    <div style="padding:16px 18px;border-bottom:1px solid rgba(148,163,184,0.14);background:rgba(2,6,23,0.45);">
                        <input id="site-search-input" type="search" placeholder="${escapeHtml(ui.placeholder)}" autocomplete="off" style="width:100%;padding:11px 14px;border-radius:8px;border:1px solid rgba(148,163,184,0.3);background:#1E293B;color:#F8FAFC;font-size:0.95rem;outline:none;margin-bottom:12px;box-sizing:border-box;"/>
                        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">
                            <label style="display:flex;flex-direction:column;gap:4px;font-size:0.78rem;color:#94A3B8;font-weight:600;">
                                ${escapeHtml(ui.catLabel)}
                                <select id="site-search-cat" style="padding:9px 10px;border-radius:8px;border:1px solid rgba(148,163,184,0.28);background:#1E293B;color:#F8FAFC;font-size:0.88rem;cursor:pointer;">${catOpts}</select>
                            </label>
                            <label style="display:flex;flex-direction:column;gap:4px;font-size:0.78rem;color:#94A3B8;font-weight:600;">
                                ${escapeHtml(ui.indLabel)}
                                <select id="site-search-ind" style="padding:9px 10px;border-radius:8px;border:1px solid rgba(148,163,184,0.28);background:#1E293B;color:#F8FAFC;font-size:0.88rem;cursor:pointer;">${indOpts}</select>
                            </label>
                        </div>
                    </div>
                    <div id="site-search-meta" style="padding:8px 18px;font-size:0.82rem;color:#94A3B8;border-bottom:1px solid rgba(148,163,184,0.1);"></div>
                    <div id="site-search-results" style="max-height:52vh;overflow-y:auto;padding:10px 14px 16px;"></div>
                </div>
            `;
            document.body.appendChild(modal);

            modal.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });
            modal.querySelector('#site-search-close').addEventListener('click', closeModal);
            const inpEl = modal.querySelector('#site-search-input');
            inpEl.addEventListener('input', renderResults);
            inpEl.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    const firstLink = modal.querySelector('#site-search-results a.site-search-item');
                    if (firstLink) {
                        e.preventDefault();
                        window.location.href = firstLink.getAttribute('href');
                    }
                }
            });
            modal.querySelector('#site-search-cat').addEventListener('change', renderResults);
            modal.querySelector('#site-search-ind').addEventListener('change', renderResults);
            return modal;
        }

        function renderResults() {
            if (!modal) return;
            const resEl = modal.querySelector('#site-search-results');
            const metaEl = modal.querySelector('#site-search-meta');
            if (!indexCache) {
                metaEl.textContent = ui.loading;
                resEl.innerHTML = '';
                return;
            }
            const q = (modal.querySelector('#site-search-input').value || '').trim().toLowerCase();
            const cat = modal.querySelector('#site-search-cat').value;
            const ind = modal.querySelector('#site-search-ind').value;
            const tokens = q ? q.split(/\s+/).filter(Boolean) : [];

            const filtered = indexCache.filter(item => {
                if (cat !== 'all' && item.c !== cat) return false;
                if (ind !== 'all' && !(item.i || []).includes(ind)) return false;
                if (tokens.length) {
                    const hay = (item.t + ' ' + item.d + ' ' + item.k).toLowerCase();
                    return tokens.every(tok => hay.includes(tok));
                }
                return true;
            });

            metaEl.textContent = ui.count(filtered.length);
            if (!filtered.length) {
                const rfqHref = document.getElementById('rfq-section') ? '#rfq-section' : (document.getElementById('contact') ? '#contact' : './#contact');
                const lineHtml = ui.lineBtn ? `<a href="https://line.me/R/ti/p/@682wvagy" target="_blank" rel="noopener noreferrer" style="display:inline-block;padding:9px 14px;border-radius:8px;background:#06C755;color:#fff;font-weight:700;font-size:0.86rem;text-decoration:none;">${escapeHtml(ui.lineBtn)}</a>` : '';
                resEl.innerHTML = `
                    <div style="text-align:center;padding:24px 12px;">
                        <p style="color:#F8FAFC;font-weight:700;margin:0 0 8px;">${escapeHtml(ui.emptyTitle)}</p>
                        <p style="color:#94A3B8;font-size:0.88rem;margin:0 0 16px;">${escapeHtml(ui.emptyDesc)}</p>
                        <div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center;">
                            ${lineHtml}
                            <a href="${rfqHref}" id="site-search-empty-rfq" style="display:inline-block;padding:9px 14px;border-radius:8px;background:#D4A843;color:#0A0F1C;font-weight:700;font-size:0.86rem;text-decoration:none;">${escapeHtml(ui.rfqBtn)}</a>
                        </div>
                    </div>
                `;
                const rfqLink = resEl.querySelector('#site-search-empty-rfq');
                if (rfqLink && rfqHref.startsWith('#')) {
                    rfqLink.addEventListener('click', () => closeModal());
                }
                return;
            }

            const curFile = (window.location.pathname.split('/').pop() || '');
            const isCurrent = (u) => (u === './' && (curFile === '' || curFile === 'index.html')) || (u === curFile);
            filtered.sort((a, b) => (isCurrent(a.u) ? 1 : 0) - (isCurrent(b.u) ? 1 : 0));

            resEl.innerHTML = filtered.map(item => `
                <a class="site-search-item" href="${escapeHtml(item.u)}">
                    <div style="min-width:0;flex:1;">
                        <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;flex-wrap:wrap;">
                            <span style="font-size:0.72rem;font-weight:700;padding:2px 8px;border-radius:999px;background:rgba(212,168,67,0.16);color:#D4A843;flex-shrink:0;">${escapeHtml(ui.catTag[item.c] || item.c)}</span>
                            <strong style="color:#F8FAFC;font-size:0.93rem;">${escapeHtml(item.t)}</strong>
                        </div>
                        <p style="margin:0;color:#94A3B8;font-size:0.82rem;line-height:1.5;">${escapeHtml(item.d)}</p>
                    </div>
                    <span style="flex-shrink:0;padding:6px 11px;border-radius:6px;background:rgba(212,168,67,0.18);border:1px solid rgba(212,168,67,0.45);color:#FDE68A;font-size:0.8rem;font-weight:700;white-space:nowrap;">${escapeHtml(ui.goLabel)}</span>
                </a>
            `).join('');
        }

        function openModal() {
            const m = ensureModal();
            m.style.display = 'block';
            document.body.style.overflow = 'hidden';
            const inp = m.querySelector('#site-search-input');
            setTimeout(() => inp && inp.focus(), 30);
            if (!indexCache) {
                renderResults();
                const idxUrl = (sLang === 'zh' ? 'js/search-index.json' : '../js/search-index.json') + '?v=20261119c';
                fetch(idxUrl).then(r => r.json()).then(data => {
                    indexCache = data[sLang] || [];
                    renderResults();
                }).catch(() => {
                    indexCache = [];
                    renderResults();
                });
            } else {
                renderResults();
            }
        }

        function closeModal() {
            if (!modal) return;
            modal.style.display = 'none';
            document.body.style.overflow = '';
        }

        trigger.addEventListener('click', openModal);
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
                e.preventDefault();
                openModal();
            } else if (e.key === 'Escape' && modal && modal.style.display === 'block') {
                closeModal();
            }
        });
    })();
});

// =========================================================================
// GA4 Lazy Loader & B2B Conversion Event Tracking (G-WR9QWTTL46)
// Zero-blocking: queues events immediately in dataLayer, loads gtag.js
// only on first user interaction or idle after load (preserves PageSpeed).
// =========================================================================
(function () {
    const GA_ID = 'G-WR9QWTTL46';
    const host = window.location.hostname || '';
    if (!host || host === 'localhost' || host === '127.0.0.1' || window.location.protocol === 'file:') {
        return;
    }

    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    if (typeof window.gtag !== 'function') {
        window.gtag = gtag;
    }

    let gaLoaded = false;
    const isDebugMode = /(?:^|[?&])ga_debug=1(?:&|$)/.test(window.location.search || '');
    function loadGA4() {
        if (gaLoaded) return;
        gaLoaded = true;
        try {
            window.gtag('js', new Date());
            const cfg = { anonymize_ip: true };
            if (isDebugMode) cfg.debug_mode = true;
            window.gtag('config', GA_ID, cfg);
            const s = document.createElement('script');
            s.async = true;
            s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
            document.head.appendChild(s);
        } catch (err) {}
    }

    ['pointerdown', 'keydown', 'scroll', 'touchstart'].forEach((evt) => {
        window.addEventListener(evt, loadGA4, { once: true, passive: true });
    });
    window.addEventListener('load', () => {
        if ('requestIdleCallback' in window) {
            window.requestIdleCallback(loadGA4, { timeout: 3000 });
        } else {
            setTimeout(loadGA4, 3000);
        }
    }, { once: true });

    const pagePath = window.location.pathname || '/';
    const pageLang = pagePath.startsWith('/en/') ? 'en' : (pagePath.startsWith('/ja/') ? 'ja' : 'zh');

    function trackEvent(eventName, params) {
        try {
            loadGA4();
            if (typeof window.gtag === 'function') {
                const payload = Object.assign({
                    page_lang: pageLang,
                    page_path: pagePath
                }, params || {});
                if (isDebugMode) payload.debug_mode = true;
                window.gtag('event', eventName, payload);
            }
        } catch (err) {}
    }

    // Fired ONLY from verified EmailJS / FormSubmit success callbacks (zero PII)
    window.JH_TrackLeadSuccess = function (formId, deliveryMethod) {
        trackEvent('generate_lead', {
            currency: 'TWD',
            form_id: formId || 'unknown_form',
            delivery_method: deliveryMethod || 'emailjs'
        });
    };

    document.addEventListener('click', (e) => {
        const el = e.target && e.target.closest ? e.target.closest('a, button, [data-copy-email]') : null;
        if (!el) return;

        if (el.hasAttribute('data-copy-email')) {
            trackEvent('click_email', { contact_method: 'copy_button' });
            return;
        }

        const href = (el.getAttribute('href') || '').trim();
        if (!href) return;

        if (/\.pdf(\?|$)/i.test(href)) {
            const parts = href.split('?')[0].split('/');
            trackEvent('pdf_download', { file_name: parts[parts.length - 1] || 'document.pdf' });
        } else if (href.indexOf('line.me') !== -1) {
            trackEvent('click_line', { channel: 'line_oa' });
        } else if (href.toLowerCase().startsWith('tel:')) {
            trackEvent('click_phone', { channel: 'tel_link' });
        } else if (href.toLowerCase().startsWith('mailto:')) {
            trackEvent('click_email', { contact_method: 'mailto_link' });
        }
    }, { passive: true });
})();



