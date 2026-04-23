document.addEventListener('DOMContentLoaded', () => {
  const slides = document.querySelectorAll('.slide');
  const dots = document.querySelectorAll('.nav-dot');
  const counter = document.getElementById('slide-counter');
  let currentSlide = 0;
  let currentStep = 0;
  let isTransitioning = false;

  function getMaxSteps(slide) {
    return parseInt(slide.dataset.steps || '0');
  }

  function showStep(slide, step) {
    slide.querySelectorAll(`[data-step="${step}"]`).forEach(el => {
      el.classList.add('visible');
    });
    // Trigger special animations
    if (slide.id === 'slide-how-it-works') {
      if (step === 3) triggerScanLine();
      if (step === 5) showOverlaps();
      if (step === 6) showTokenCounts();
    }
  }

  function hideAllSteps(slide) {
    slide.querySelectorAll('[data-step]').forEach(el => {
      el.classList.remove('visible');
    });
    // Reset special animations
    const scanLine = slide.querySelector('.scan-line');
    if (scanLine) scanLine.classList.remove('animate');
    slide.querySelectorAll('.overlap-marker').forEach(m => m.classList.remove('show'));
    slide.querySelectorAll('.token-count').forEach(t => t.classList.remove('show'));
  }

  function goToSlide(index) {
    if (index < 0 || index >= slides.length || isTransitioning) return;
    isTransitioning = true;

    const prev = slides[currentSlide];
    const next = slides[index];

    // Hide all steps on the slide we're leaving
    hideAllSteps(prev);

    // Determine direction
    const direction = index > currentSlide ? 1 : -1;

    prev.classList.remove('active');
    prev.classList.add(direction > 0 ? 'exit-left' : '');
    prev.style.transform = direction > 0 ? 'translateX(-60px)' : 'translateX(60px)';
    prev.style.opacity = '0';

    next.style.transform = direction > 0 ? 'translateX(60px)' : 'translateX(-60px)';
    next.style.opacity = '0';
    next.classList.remove('exit-left');
    next.style.visibility = 'visible';

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        next.classList.add('active');
        next.style.transform = '';
        next.style.opacity = '';
        prev.style.visibility = '';
        prev.style.transform = '';
        prev.style.opacity = '';
      });
    });

    currentSlide = index;
    currentStep = 0;

    // Update nav
    dots.forEach((d, i) => d.classList.toggle('active', i === index));
    counter.textContent = `${index + 1} / ${slides.length}`;

    setTimeout(() => { isTransitioning = false; }, 650);
  }

  function advance() {
    const slide = slides[currentSlide];
    const maxSteps = getMaxSteps(slide);

    if (currentStep < maxSteps) {
      currentStep++;
      showStep(slide, currentStep);
    } else if (currentSlide < slides.length - 1) {
      goToSlide(currentSlide + 1);
    }
  }

  function retreat() {
    if (currentStep > 0) {
      // Hide current step
      const slide = slides[currentSlide];
      slide.querySelectorAll(`[data-step="${currentStep}"]`).forEach(el => {
        el.classList.remove('visible');
      });
      currentStep--;
    } else if (currentSlide > 0) {
      goToSlide(currentSlide - 1);
      // Show all steps of previous slide
      const prevSlide = slides[currentSlide];
      const max = getMaxSteps(prevSlide);
      for (let i = 1; i <= max; i++) {
        showStep(prevSlide, i);
      }
      currentStep = max;
    }
  }

  // Special animation triggers
  function triggerScanLine() {
    const scanLine = document.querySelector('.scan-line');
    if (scanLine) {
      scanLine.classList.remove('animate');
      void scanLine.offsetWidth; // force reflow
      scanLine.classList.add('animate');
    }
  }

  function showOverlaps() {
    document.querySelectorAll('.overlap-marker').forEach((m, i) => {
      setTimeout(() => m.classList.add('show'), i * 200);
    });
    document.querySelectorAll('.overlap-text').forEach(t => {
      t.style.color = 'var(--white)';
    });
  }

  function showTokenCounts() {
    document.querySelectorAll('.token-count').forEach((t, i) => {
      setTimeout(() => t.classList.add('show'), i * 150);
    });
  }

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Enter') {
      e.preventDefault();
      advance();
    } else if (e.key === 'ArrowLeft' || e.key === 'Backspace') {
      e.preventDefault();
      retreat();
    } else if (e.key === 'f' || e.key === 'F') {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
      } else {
        document.exitFullscreen();
      }
    }
  });

  // Click navigation
  document.querySelector('.nav-arrow-btn.left')?.addEventListener('click', retreat);
  document.querySelector('.nav-arrow-btn.right')?.addEventListener('click', advance);

  // Dot navigation
  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => goToSlide(i));
  });

  // Touch support
  let touchStartX = 0;
  document.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; });
  document.addEventListener('touchend', (e) => {
    const diff = touchStartX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 50) {
      diff > 0 ? advance() : retreat();
    }
  });

  // Initialize first slide
  counter.textContent = `1 / ${slides.length}`;
});
