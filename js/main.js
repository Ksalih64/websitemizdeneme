/**
 * KMZ Trade - Premium Website JavaScript
 * Advanced animations, particles, and interactions
 */

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
  initPreloader();
  initParticles();
  initHeader();
  initMobileMenu();
  initScrollProgress();
  initScrollAnimations();
  initTabs();
  initFAQ();
  initCounters();
  initSmoothScroll();
  initFormEnhancements();
  initBackToTop();
  initCookieBanner();
  initLanguageSwitcher();
  initCatalogDownloader();
  initCatalogPdfLinks();
});

// ============================================
// PRELOADER
// ============================================
function initPreloader() {
  const preloader = document.getElementById('preloader');
  if (!preloader) return;

  window.addEventListener('load', function () {
    setTimeout(() => {
      preloader.classList.add('hidden');
      setTimeout(() => preloader.remove(), 500);
    }, 800);
  });
}

// ============================================
// PARTICLES BACKGROUND
// ============================================
function initParticles() {
  const config = {
    particles: {
      number: { value: 60, density: { enable: true, value_area: 1000 } },
      color: { value: ['#d4a855', '#f0d078', '#bc8c3d'] },
      shape: { type: 'circle' },
      opacity: {
        value: 0.4,
        random: true,
        anim: { enable: true, speed: 0.8, opacity_min: 0.1, sync: false }
      },
      size: {
        value: 3,
        random: true,
        anim: { enable: true, speed: 2, size_min: 0.5, sync: false }
      },
      line_linked: {
        enable: true,
        distance: 150,
        color: '#d4a855',
        opacity: 0.15,
        width: 1
      },
      move: {
        enable: true,
        speed: 1.2,
        direction: 'none',
        random: true,
        straight: false,
        out_mode: 'out',
        bounce: false
      }
    },
    interactivity: {
      detect_on: 'canvas',
      events: {
        onhover: { enable: true, mode: 'grab' },
        onclick: { enable: true, mode: 'push' },
        resize: true
      },
      modes: {
        grab: { distance: 180, line_linked: { opacity: 0.4 } },
        push: { particles_nb: 3 }
      }
    },
    retina_detect: true
  };

  if (typeof particlesJS !== 'undefined') {
    if (document.getElementById('particles-js')) particlesJS('particles-js', config);
    if (document.getElementById('particles-bg')) particlesJS('particles-bg', config);
  }
}

// ============================================
// HEADER SCROLL EFFECTS
// ============================================
function initHeader() {
  const header = document.getElementById('header');
  if (!header) return;

  function updateHeader() {
    if (window.pageYOffset > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }

  window.addEventListener('scroll', () => requestAnimationFrame(updateHeader));
  updateHeader();
}

// ============================================
// MOBILE MENU
// ============================================
function initMobileMenu() {
  const menuBtn = document.getElementById('mobileMenuBtn');
  const navLinks = document.getElementById('navLinks');

  if (!menuBtn || !navLinks) return;

  menuBtn.addEventListener('click', function () {
    navLinks.classList.toggle('active');
    menuBtn.classList.toggle('active');
    document.body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : '';
  });

  navLinks.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function () {
      navLinks.classList.remove('active');
      menuBtn.classList.remove('active');
      document.body.style.overflow = '';
    });
  });
}

// ============================================
// SCROLL PROGRESS BAR
// ============================================
function initScrollProgress() {
  const progressBar = document.getElementById('scrollProgress');
  if (!progressBar) return;

  function updateProgress() {
    const scrollTop = window.pageYOffset;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (scrollTop / docHeight) * 100;
    progressBar.style.width = progress + '%';
  }

  window.addEventListener('scroll', () => requestAnimationFrame(updateProgress));
}

// ============================================
// SCROLL ANIMATIONS
// ============================================
function initScrollAnimations() {
  const fadeElements = document.querySelectorAll('.fade-in');
  if (!fadeElements.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -80px 0px' });

  fadeElements.forEach(el => observer.observe(el));
}

// ============================================
// TAB FUNCTIONALITY
// ============================================
function initTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  if (!tabBtns.length) return;

  tabBtns.forEach(btn => {
    btn.addEventListener('click', function () {
      const target = this.getAttribute('data-tab');

      tabBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');

      tabContents.forEach(content => {
        content.classList.remove('active');
        if (content.id === target) content.classList.add('active');
      });
    });
  });

  // Handle hash navigation
  const hash = window.location.hash.replace('#', '');
  if (hash) {
    const targetTab = document.querySelector(`[data-tab="${hash}"]`);
    if (targetTab) targetTab.click();
  }
}

// ============================================
// FAQ ACCORDION
// ============================================
function initFAQ() {
  const faqItems = document.querySelectorAll('.faq-item');
  if (!faqItems.length) return;

  faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    if (!question) return;

    question.addEventListener('click', function () {
      const isActive = item.classList.contains('active');

      // Close all others
      faqItems.forEach(i => i.classList.remove('active'));

      // Toggle current
      if (!isActive) item.classList.add('active');
    });
  });
}

// ============================================
// ANIMATED COUNTERS
// ============================================
function initCounters() {
  const counters = document.querySelectorAll('.stat-number');
  if (!counters.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(counter => observer.observe(counter));
}

function animateCounter(element) {
  const text = element.textContent;
  const match = text.match(/(\d+)/);
  if (!match) return;

  const target = parseInt(match[0]);
  const suffix = text.replace(match[0], '').trim();
  const duration = 2000;
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.floor(target * eased);

    element.textContent = current + suffix;

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      element.textContent = target + suffix;
    }
  }

  requestAnimationFrame(update);
}

// ============================================
// SMOOTH SCROLLING
// ============================================
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href === '#' || href === '') return;

      const target = document.querySelector(href);
      if (!target) return;

      e.preventDefault();

      const headerOffset = 100;
      const elementPosition = target.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

      window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
    });
  });
}

// ============================================
// FORM ENHANCEMENTS
// ============================================
function initFormEnhancements() {
  const forms = document.querySelectorAll('form');

  forms.forEach(form => {
    const inputs = form.querySelectorAll('.form-input, .form-select, .form-textarea');
    inputs.forEach(input => {
      input.addEventListener('focus', () => input.parentElement?.classList.add('focused'));
      input.addEventListener('blur', () => input.parentElement?.classList.remove('focused'));
    });

    form.addEventListener('submit', function (e) {
      if (form.id === 'contactForm') {
        e.preventDefault();
        const formData = new FormData(form);
        const productSelect = form.querySelector('#product');
        const productLabel = productSelect?.selectedOptions?.[0]?.textContent?.trim() || '';
        const urlParams = new URLSearchParams(window.location.search);
        const catalogType = urlParams.get('catalog') || '';
        const inquiryType = urlParams.get('type') || '';
        const subject = catalogType
          ? `KMZ Trade Catalog Request - ${catalogType}`
          : `KMZ Trade RFQ - ${productLabel || 'Product Inquiry'}`;
        const body = [
          `Name: ${formData.get('name') || ''}`,
          `Email: ${formData.get('email') || ''}`,
          `Company: ${formData.get('company') || ''}`,
          `Product: ${productLabel || formData.get('product') || ''}`,
          `Inquiry Type: ${inquiryType || 'rfq'}`,
          `Catalog Type: ${catalogType || ''}`,
          '',
          'Message:',
          formData.get('message') || ''
        ].join('\n');

        window.location.href = `mailto:info@kmztrade.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
        return;
      }

      const submitBtn = form.querySelector('[type="submit"]');
      if (submitBtn) {
        submitBtn.textContent = 'Wird gesendet...';
        submitBtn.disabled = true;
      }
    });
  });

  // Pre-fill product from URL
  const urlParams = new URLSearchParams(window.location.search);
  const product = urlParams.get('product');
  if (product) {
    const productSelect = document.getElementById('product');
    if (productSelect) productSelect.value = product;
  }

  const catalogType = urlParams.get('catalog');
  const inquiryType = urlParams.get('type');
  if (inquiryType === 'catalog') {
    const message = document.getElementById('message');
    if (message && !message.value) {
      const label = catalogType ? `${catalogType} catalog` : 'product catalog';
      message.value = `Please send me the ${label}.`;
    }
  }
}

// ============================================
// BACK TO TOP BUTTON
// ============================================
function initBackToTop() {
  const btn = document.getElementById('backToTop');
  if (!btn) return;

  function toggleButton() {
    if (window.pageYOffset > 400) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  }

  window.addEventListener('scroll', () => requestAnimationFrame(toggleButton));

  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ============================================
// COOKIE BANNER
// ============================================
function initCookieBanner() {
  const banner = document.getElementById('cookieBanner');
  const acceptBtn = document.getElementById('cookieAccept');
  const declineBtn = document.getElementById('cookieDecline');

  if (!banner) return;

  // Check if already accepted/declined
  if (localStorage.getItem('cookieConsent')) return;

  // Show banner after delay
  setTimeout(() => banner.classList.add('visible'), 2000);

  acceptBtn?.addEventListener('click', () => {
    localStorage.setItem('cookieConsent', 'accepted');
    banner.classList.remove('visible');
  });

  declineBtn?.addEventListener('click', () => {
    localStorage.setItem('cookieConsent', 'declined');
    banner.classList.remove('visible');
  });
}

// ============================================
// LANGUAGE SWITCHER
// ============================================
function initLanguageSwitcher() {
  const switcher = document.getElementById('langSwitcher');
  const btn = document.getElementById('langBtn');
  const dropdown = document.getElementById('langDropdown');

  if (!switcher || !btn || !dropdown) return;

  // Language data
  const langFlags = {
    de: '🇩🇪',
    en: '🇬🇧',
    tr: '🇹🇷'
  };

  // Get saved language or default to German
  let currentLang = localStorage.getItem('kmzLang') || 'de';

  // Update button display
  function updateButton(lang) {
    const flag = btn.querySelector('.lang-flag');
    const code = btn.querySelector('.lang-code');
    if (flag) flag.textContent = langFlags[lang];
    if (code) code.textContent = lang.toUpperCase();
  }

  // Toggle dropdown
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    switcher.classList.toggle('active');
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!switcher.contains(e.target)) {
      switcher.classList.remove('active');
    }
  });

  // Handle language selection
  dropdown.querySelectorAll('.lang-option').forEach(option => {
    option.addEventListener('click', () => {
      const lang = option.dataset.lang;

      // Update active state
      dropdown.querySelectorAll('.lang-option').forEach(o => o.classList.remove('active'));
      option.classList.add('active');

      // Update button
      updateButton(lang);

      // Save preference
      localStorage.setItem('kmzLang', lang);
      currentLang = lang;

      // Apply translations
      applyTranslations(lang);
      updateCatalogPdfLinks(lang);
      applyCatalogSpecTranslations(lang);

      // Close dropdown
      switcher.classList.remove('active');
    });
  });

  // Apply saved language on load
  updateButton(currentLang);
  dropdown.querySelector(`[data-lang="${currentLang}"]`)?.classList.add('active');

  // Keep fallback HTML and translation data in sync for every language, including German.
  if (typeof translations !== 'undefined') {
    applyTranslations(currentLang);
  }

  updateCatalogPdfLinks(currentLang);
  applyCatalogSpecTranslations(currentLang);
}

// Apply translations to elements with data-i18n attribute
function applyTranslations(lang) {
  if (typeof translations === 'undefined') return;

  const t = translations[lang];
  if (!t) return;

  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (t[key]) {
      if (el.tagName === 'INPUT' && (el.type === 'submit' || el.type === 'button')) {
        el.value = t[key];
      } else {
        el.textContent = t[key];
      }
    }
  });

  // Handle placeholders
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.dataset.i18nPlaceholder;
    if (t[key]) {
      el.placeholder = t[key];
    }
  });

  document.querySelectorAll('[data-i18n-label]').forEach(el => {
    const key = el.dataset.i18nLabel;
    if (t[key]) {
      el.label = t[key];
    }
  });

  // Update HTML lang attribute
  document.documentElement.lang = lang === 'de' ? 'de' : (lang === 'en' ? 'en' : 'tr');
  applyCatalogSpecTranslations(lang);
}

const catalogPdfFiles = {
  de: {
    full: 'assets/catalogs/kmz-trade-full-catalog-de.pdf',
    minerals: 'assets/catalogs/kmz-trade-minerals-catalog-de.pdf',
    food: 'assets/catalogs/kmz-trade-food-catalog-de.pdf'
  },
  en: {
    full: 'assets/catalogs/kmz-trade-full-catalog-en.pdf',
    minerals: 'assets/catalogs/kmz-trade-minerals-catalog-en.pdf',
    food: 'assets/catalogs/kmz-trade-food-catalog-en.pdf'
  },
  tr: {
    full: 'assets/catalogs/kmz-trade-full-catalog-tr.pdf',
    minerals: 'assets/catalogs/kmz-trade-minerals-catalog-tr.pdf',
    food: 'assets/catalogs/kmz-trade-food-catalog-tr.pdf'
  }
};

const catalogSpecTranslations = {
  de: {
    labels: {
      main: 'Hauptbestandteil',
      quality: 'Qualität',
      form: 'Lieferform',
      packaging: 'Verpackung',
      docs: 'Dokumente'
    },
    analysis: 'Analysebericht verfügbar',
    docs: 'Analysebericht, COA, Herkunft und Versandpapiere verfügbar',
    products: {
      manganese: {
        main: 'Manganerz',
        form: 'Erz / Konzentrat',
        packaging: 'Bulk oder Big Bag',
        apps: ['Stahl', 'Legierungen', 'Batterie']
      },
      lead: {
        main: 'Bleierz',
        form: 'Erz / Konzentrat',
        packaging: 'Bulk oder Big Bag',
        apps: ['Batterien', 'Metallurgie', 'Industrie']
      },
      monazite: {
        main: 'Monazit',
        form: 'Mineralsand / Konzentrat',
        packaging: 'Bulk oder Big Bag',
        apps: ['Seltene Erden', 'Technologie', 'Industrie']
      },
      columbite: {
        main: 'Columbit',
        form: 'Erz / Konzentrat',
        packaging: 'Bulk oder Big Bag',
        apps: ['Elektronik', 'Superlegierung', 'Niob']
      },
      zirconium: {
        main: 'Zirconium',
        form: 'Mineralsand',
        packaging: 'Bulk oder Big Bag',
        apps: ['Keramik', 'Gießerei', 'Refraktär']
      }
    }
  },
  en: {
    labels: {
      main: 'Main component',
      quality: 'Quality basis',
      form: 'Delivery form',
      packaging: 'Packaging',
      docs: 'Documents'
    },
    analysis: 'Analysis report available',
    docs: 'Analysis report, COA, origin and shipment papers available',
    products: {
      manganese: {
        main: 'Manganese ore',
        form: 'Ore / concentrate',
        packaging: 'Bulk or Big Bag',
        apps: ['Steel', 'Alloys', 'Battery']
      },
      lead: {
        main: 'Lead ore',
        form: 'Ore / concentrate',
        packaging: 'Bulk or Big Bag',
        apps: ['Batteries', 'Metallurgy', 'Industry']
      },
      monazite: {
        main: 'Monazite',
        form: 'Mineral sand / concentrate',
        packaging: 'Bulk or Big Bag',
        apps: ['Rare earths', 'Technology', 'Industry']
      },
      columbite: {
        main: 'Columbite',
        form: 'Ore / concentrate',
        packaging: 'Bulk or Big Bag',
        apps: ['Electronics', 'Superalloys', 'Niobium']
      },
      zirconium: {
        main: 'Zirconium',
        form: 'Mineral sand',
        packaging: 'Bulk or Big Bag',
        apps: ['Ceramics', 'Foundry', 'Refractory']
      }
    }
  },
  tr: {
    labels: {
      main: 'Ana bileşen',
      quality: 'Kalite temeli',
      form: 'Teslim formu',
      packaging: 'Ambalaj',
      docs: 'Belgeler'
    },
    analysis: 'Analiz raporu mevcut',
    docs: 'Analiz raporu, COA, menşe ve sevkiyat evrakları mevcut',
    products: {
      manganese: {
        main: 'Manganez cevheri',
        form: 'Cevher / konsantre',
        packaging: 'Bulk veya Big Bag',
        apps: ['Çelik', 'Alaşımlar', 'Batarya']
      },
      lead: {
        main: 'Kurşun cevheri',
        form: 'Cevher / konsantre',
        packaging: 'Bulk veya Big Bag',
        apps: ['Batarya', 'Metalurji', 'Sanayi']
      },
      monazite: {
        main: 'Monazite',
        form: 'Mineral kumu / konsantre',
        packaging: 'Bulk veya Big Bag',
        apps: ['Nadir topraklar', 'Teknoloji', 'Sanayi']
      },
      columbite: {
        main: 'Columbite',
        form: 'Cevher / konsantre',
        packaging: 'Bulk veya Big Bag',
        apps: ['Elektronik', 'Süper alaşım', 'Niyobyum']
      },
      zirconium: {
        main: 'Zirconium',
        form: 'Mineral kumu',
        packaging: 'Bulk veya Big Bag',
        apps: ['Seramik', 'Döküm', 'Refrakter']
      }
    }
  }
};

function getActiveLanguage() {
  const lang = localStorage.getItem('kmzLang') || document.documentElement.lang || 'de';
  return catalogPdfFiles[lang] ? lang : 'de';
}

function updateCatalogPdfLinks(lang = getActiveLanguage()) {
  const language = catalogPdfFiles[lang] ? lang : 'de';

  document.querySelectorAll('.catalog-pdf-link').forEach(link => {
    const catalogType = link.getAttribute('data-catalog-type') || 'full';
    const href = catalogPdfFiles[language][catalogType];
    if (!href) return;

    link.setAttribute('href', href);
    link.setAttribute('download', href.split('/').pop());
  });
}

function applyCatalogSpecTranslations(lang = getActiveLanguage()) {
  const language = catalogSpecTranslations[lang] ? lang : 'de';
  const spec = catalogSpecTranslations[language];

  document.querySelectorAll('.catalog-card').forEach(card => {
    const heading = card.querySelector('.catalog-card-header h3[data-i18n]');
    const productKey = heading?.dataset.i18n?.replace('product.', '');
    const product = spec.products[productKey];
    if (!product) return;

    const rows = card.querySelectorAll('.catalog-spec-table tr');
    const rowData = [
      [spec.labels.main, product.main],
      [spec.labels.quality, spec.analysis],
      [spec.labels.form, product.form],
      [spec.labels.packaging, product.packaging],
      [spec.labels.docs, spec.docs]
    ];

    rows.forEach((row, index) => {
      const cells = row.querySelectorAll('td');
      const data = rowData[index];
      if (cells.length < 2 || !data) return;
      cells[0].textContent = data[0];
      cells[1].textContent = data[1];
    });

    card.querySelectorAll('.catalog-app-tag').forEach((tag, index) => {
      if (product.apps[index]) tag.textContent = product.apps[index];
    });
  });
}

// ============================================
// CATALOG PDF DOWNLOADER
// ============================================
function initCatalogDownloader() {
  const btn = document.getElementById('downloadPdfBtn');
  if (!btn) return;

  btn.addEventListener('click', function () {
    // Don't prevent default — let the browser download natively via the download attribute
    const originalContent = btn.innerHTML;
    btn.style.width = btn.offsetWidth + 'px';
    btn.innerHTML = '<span style="display:inline-block; animation: rotate 1s linear infinite; margin-right: 8px;">...</span> Wird heruntergeladen...';

    setTimeout(() => {
      btn.innerHTML = 'Download bereit';
      btn.style.background = 'var(--accent-gold)';
      btn.style.color = 'var(--primary-bg)';
      
      setTimeout(() => {
        btn.innerHTML = originalContent;
        btn.style.background = '';
        btn.style.color = '';
        btn.style.width = '';
      }, 2500);
    }, 1500);
  });
}

function initCatalogPdfLinks() {
  const links = document.querySelectorAll('.catalog-pdf-link');
  updateCatalogPdfLinks();
  if (!links.length) return;

  links.forEach(link => {
    link.addEventListener('click', async function (event) {
      const href = link.getAttribute('href');
      if (!href) return;

      try {
        const response = await fetch(href, { method: 'HEAD' });
        if (response.ok) return;
      } catch (error) {
        // Fall through to RFQ redirect when local/static hosting cannot verify the PDF.
      }

      event.preventDefault();
      const catalogType = link.getAttribute('data-catalog-type') || 'catalog';
      window.location.href = `contact.html?type=catalog&catalog=${encodeURIComponent(catalogType)}`;
    });
  });
}

// Helper animation for spinner
const style = document.createElement('style');
style.textContent = `
  @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
`;
document.head.appendChild(style);
