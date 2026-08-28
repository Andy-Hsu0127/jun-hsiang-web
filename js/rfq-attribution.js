/**
 * Jun-Hsiang RFQ Attribution Engine v1.0
 * Lightweight, session-scoped touchpoint tracking for B2B engineering RFQ attribution
 */
(function() {
    'use strict';
    
    const ATTR_KEY = 'jh_rfq_attribution_v1';
    const ATTR_VERSION = 'v1';
    
    function getClusterFromPath(path) {
        const p = path.toLowerCase();
        if (p.includes('overmolding') || p.includes('vibration')) return 'overmolding';
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
            const initialSource = getTrafficSource(referrer);
            
            attr = {
                version: ATTR_VERSION,
                session_id: 'sess_' + Math.random().toString(36).substring(2, 9) + '_' + Math.floor(now / 1000),
                session_start_time: now,
                first_page: currentPath,
                first_source: initialSource,
                referrer: referrer,
                utm_source: urlParams.get('utm_source') || '',
                utm_medium: urlParams.get('utm_medium') || '',
                utm_campaign: urlParams.get('utm_campaign') || '',
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
        
        return {
            rfq_first_page: attr.first_page || window.location.pathname,
            rfq_first_source: attr.first_source || 'direct',
            rfq_first_content: attr.first_content_touch || '(none)',
            rfq_last_content: attr.last_content_touch || '(none)',
            rfq_source_cluster: attr.source_cluster || 'general_factory',
            rfq_conversion_page: window.location.pathname,
            rfq_referrer: attr.referrer || '(direct)',
            rfq_utm_source: attr.utm_source || '(none)',
            rfq_utm_medium: attr.utm_medium || '(none)',
            rfq_utm_campaign: attr.utm_campaign || '(none)',
            rfq_session_id: attr.session_id || '',
            rfq_session_duration_sec: durationSec,
            rfq_journey_path: (attr.journey || []).join(' -> '),
            rfq_attribution_version: attr.version || ATTR_VERSION
        };
    }

    function populateFormFields() {
        const payload = getAttributionPayload();
        
        const forms = document.querySelectorAll('#contact-form, #general-contact-form');
        forms.forEach(form => {
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

    window.JH_Attribution = {
        getPayload: getAttributionPayload,
        populateForms: populateFormFields
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', populateFormFields);
    } else {
        populateFormFields();
    }
})();
