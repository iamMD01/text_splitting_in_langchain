document.addEventListener('DOMContentLoaded', () => {
  const slides = document.querySelectorAll('.slide');
  const dots = document.querySelectorAll('.nav-dot');
  const counter = document.getElementById('slide-counter');
  let currentSlide = 0;
  let currentStep = 0;
  let isTransitioning = false;

  function isManual(slide) {
    return slide.classList.contains('manual-steps');
  }

  function getMaxSteps(slide) {
    return parseInt(slide.dataset.steps || '0');
  }

  function showStep(slide, step) {
    slide.querySelectorAll(`[data-step="${step}"]`).forEach(el => {
      el.classList.add('visible');
    });
    if (slide.id === 'slide-how-it-works') {
      if (step === 3) triggerScanLine();
      if (step === 4) triggerChunksAnimation();
      if (step === 5) showOverlaps();
      if (step === 6) showTokenCounts();
    }
  }

  function hideAllSteps(slide) {
    slide.querySelectorAll('[data-step]').forEach(el => {
      el.classList.remove('visible');
    });
    const scanLine = slide.querySelector('.scan-line');
    if (scanLine) scanLine.classList.remove('animate');
    slide.querySelectorAll('.overlap-marker').forEach(m => m.classList.remove('show'));
    slide.querySelectorAll('.token-count').forEach(t => t.classList.remove('show'));
    const originalText = slide.querySelector('.original-text-block');
    if (originalText) originalText.classList.remove('fade-out');
    const chunksResult = slide.querySelector('.chunks-result');
    if (chunksResult) chunksResult.classList.remove('visible');
  }

  function goToSlide(index) {
    if (index < 0 || index >= slides.length || isTransitioning) return;
    isTransitioning = true;

    const prev = slides[currentSlide];
    const next = slides[index];
    const direction = index > currentSlide ? 1 : -1;

    hideAllSteps(prev);

    prev.classList.remove('active');
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

    dots.forEach((d, i) => d.classList.toggle('active', i === index));
    counter.textContent = `${index + 1} / ${slides.length}`;

    setTimeout(() => { isTransitioning = false; }, 650);
  }

  function advance() {
    const slide = slides[currentSlide];
    const maxSteps = getMaxSteps(slide);

    if (isManual(slide) && currentStep < maxSteps) {
      currentStep++;
      showStep(slide, currentStep);
    } else if (currentSlide < slides.length - 1) {
      goToSlide(currentSlide + 1);
    }
  }

  function retreat() {
    const slide = slides[currentSlide];

    if (isManual(slide) && currentStep > 0) {
      slide.querySelectorAll(`[data-step="${currentStep}"]`).forEach(el => {
        el.classList.remove('visible');
      });
      // Reset special states when stepping back
      if (currentStep === 4) {
        const chunksResult = slide.querySelector('.chunks-result');
        if (chunksResult) chunksResult.classList.remove('visible');
      }
      if (currentStep === 3) {
        const originalText = slide.querySelector('.original-text-block');
        if (originalText) originalText.classList.remove('fade-out');
        const scanLine = slide.querySelector('.scan-line');
        if (scanLine) scanLine.classList.remove('animate');
      }
      currentStep--;
    } else if (currentSlide > 0) {
      const targetIndex = currentSlide - 1;
      goToSlide(targetIndex);
      // If going back to a manual slide, show all its steps
      const targetSlide = slides[targetIndex];
      if (isManual(targetSlide)) {
        const max = getMaxSteps(targetSlide);
        for (let i = 1; i <= max; i++) {
          showStep(targetSlide, i);
        }
        currentStep = max;
      }
    }
  }

  // Special animation triggers
  function triggerScanLine() {
    const scanLine = document.querySelector('.scan-line');
    const originalText = document.getElementById('original-text');
    if (scanLine) {
      scanLine.classList.remove('animate');
      void scanLine.offsetWidth;
      scanLine.classList.add('animate');
    }
    if (originalText) {
      setTimeout(() => originalText.classList.add('fade-out'), 1800);
    }
  }

  function showOverlaps() {
    document.querySelectorAll('.overlap-marker').forEach((m, i) => {
      setTimeout(() => m.classList.add('show'), i * 300);
    });
  }

  function showTokenCounts() {
    document.querySelectorAll('.token-count').forEach((t, i) => {
      setTimeout(() => t.classList.add('show'), i * 200);
    });
  }

  function triggerChunksAnimation() {
    const chunksResult = document.querySelector('.chunks-result');
    if (chunksResult) chunksResult.classList.add('visible');
  }

  // Keyboard
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

  // Button clicks (using IDs now)
  document.getElementById('btn-prev')?.addEventListener('click', retreat);
  document.getElementById('btn-next')?.addEventListener('click', advance);

  // Dot navigation
  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => goToSlide(i));
  });

  // Touch
  let touchStartX = 0;
  document.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; });
  document.addEventListener('touchend', (e) => {
    const diff = touchStartX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 50) {
      diff > 0 ? advance() : retreat();
    }
  });

  counter.textContent = `1 / ${slides.length}`;
});
