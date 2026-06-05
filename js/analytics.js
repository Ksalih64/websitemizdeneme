/**
 * KMZ Trade analytics integration.
 * Uses GA4 with consent-aware loading for EU-friendly visitor measurement.
 */
(function () {
  const measurementId = 'G-0T769P742C';
  const consentKey = 'cookieConsent';
  const consentRequiredRegions = [
    'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR',
    'HU', 'IS', 'IE', 'IT', 'LV', 'LI', 'LT', 'LU', 'MT', 'NL', 'NO', 'PL',
    'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'GB', 'CH'
  ];
  let runtimeConsentChoice = null;

  window.dataLayer = window.dataLayer || [];

  function gtag() {
    window.dataLayer.push(arguments);
  }

  window.gtag = window.gtag || gtag;

  function getStoredConsent() {
    if (runtimeConsentChoice) return runtimeConsentChoice;

    try {
      return localStorage.getItem(consentKey);
    } catch (_) {
      return null;
    }
  }

  function consentStateForOtherRegions() {
    return getStoredConsent() === 'declined' ? 'denied' : 'granted';
  }

  function consentStateForConsentRegions() {
    return getStoredConsent() === 'accepted' ? 'granted' : 'denied';
  }

  function shouldSendMeasurementEvents() {
    return getStoredConsent() !== 'declined';
  }

  window.gtag('consent', 'default', {
    analytics_storage: consentStateForOtherRegions(),
    ad_storage: consentStateForOtherRegions(),
    ad_user_data: consentStateForOtherRegions(),
    ad_personalization: consentStateForOtherRegions(),
    functionality_storage: 'granted',
    security_storage: 'granted',
    wait_for_update: 500
  });

  window.gtag('consent', 'default', {
    analytics_storage: consentStateForConsentRegions(),
    ad_storage: consentStateForConsentRegions(),
    ad_user_data: consentStateForConsentRegions(),
    ad_personalization: consentStateForConsentRegions(),
    functionality_storage: 'granted',
    security_storage: 'granted',
    wait_for_update: 500,
    region: consentRequiredRegions
  });

  const googleTag = document.createElement('script');
  googleTag.async = true;
  googleTag.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
  document.head.appendChild(googleTag);

  window.gtag('js', new Date());
  window.gtag('config', measurementId, {
    send_page_view: shouldSendMeasurementEvents()
  });

  window.kmzUpdateAnalyticsConsent = function (accepted) {
    runtimeConsentChoice = accepted ? 'accepted' : 'declined';

    window.gtag('consent', 'update', {
      analytics_storage: accepted ? 'granted' : 'denied',
      ad_storage: accepted ? 'granted' : 'denied',
      ad_user_data: accepted ? 'granted' : 'denied',
      ad_personalization: accepted ? 'granted' : 'denied'
    });

    if (accepted) {
      window.gtag('event', 'page_view', {
        page_title: document.title,
        page_location: window.location.href,
        page_path: window.location.pathname
      });
    }
  };

  window.kmzTrackEvent = function (eventName, params = {}) {
    if (!shouldSendMeasurementEvents()) return;

    window.gtag('event', eventName, {
      page_title: document.title,
      page_location: window.location.href,
      ...params
    });
  };

  function getLinkLabel(link) {
    return (link.textContent || link.getAttribute('aria-label') || link.href || '').trim().slice(0, 120);
  }

  function trackClick(event) {
    const link = event.target.closest('a[href]');
    const langButton = event.target.closest('.lang-option[data-lang]');

    if (langButton) {
      window.kmzTrackEvent('language_change', {
        language: langButton.dataset.lang
      });
      return;
    }

    if (!link) return;

    const href = link.getAttribute('href') || '';
    const absoluteHref = link.href || href;
    const label = getLinkLabel(link);

    if (/\.pdf(\?|#|$)/i.test(href)) {
      window.kmzTrackEvent('file_download', {
        file_name: href.split('/').pop(),
        file_extension: 'pdf',
        link_url: absoluteHref,
        catalog_type: link.dataset.catalogType || 'unknown'
      });
      return;
    }

    if (href.startsWith('mailto:')) {
      window.kmzTrackEvent('email_click', {
        link_text: label,
        link_url: href
      });
      return;
    }

    if (href.includes('contact.html') || link.dataset.i18n === 'nav.cta' || link.dataset.i18n === 'product.inquiry') {
      window.kmzTrackEvent('lead_click', {
        link_text: label,
        link_url: absoluteHref
      });
    }
  }

  function trackFormSubmit(event) {
    const form = event.target;
    if (!(form instanceof HTMLFormElement)) return;

    window.kmzTrackEvent('form_submit', {
      form_id: form.id || 'contact_form',
      form_name: form.getAttribute('name') || form.id || 'contact_form'
    });
  }

  function trackVideoPlay(event) {
    const video = event.target;
    if (!(video instanceof HTMLVideoElement) || video.dataset.analyticsStarted === 'true') return;

    video.dataset.analyticsStarted = 'true';
    window.kmzTrackEvent('video_start', {
      video_url: video.currentSrc || video.getAttribute('src') || 'unknown'
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.addEventListener('click', trackClick);
    document.addEventListener('submit', trackFormSubmit);
    document.querySelectorAll('video').forEach(video => {
      video.addEventListener('play', trackVideoPlay);
    });
  });
})();
