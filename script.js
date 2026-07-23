(() => {
  const nav = document.getElementById("nav");
  const reveals = document.querySelectorAll(".reveal");
  const videos = document.querySelectorAll(".tiempo__player");

  const onScroll = () => {
    if (!nav) return;
    nav.classList.toggle("is-solid", window.scrollY > 40);
  };

  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  const lockMute = (video) => {
    if (video.muted && video.volume === 0) return;
    video.muted = true;
    video.defaultMuted = true;
    video.setAttribute("muted", "");
    video.volume = 0;
  };

  videos.forEach((video) => {
    lockMute(video);
    video.addEventListener("volumechange", () => lockMute(video));
    video.addEventListener("play", () => lockMute(video));
  });

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.14, rootMargin: "0px 0px -8% 0px" }
    );
    reveals.forEach((el) => io.observe(el));

    if (videos.length) {
      const vio = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            const video = entry.target;
            if (entry.isIntersecting) {
              lockMute(video);
              video.play().catch(() => {});
            } else {
              video.pause();
            }
          });
        },
        { threshold: 0.35 }
      );

      videos.forEach((video) => vio.observe(video));
    }
  } else {
    reveals.forEach((el) => el.classList.add("is-in"));
  }

  document.querySelectorAll("[data-carousel]").forEach((root) => {
    const slides = Array.from(root.querySelectorAll(".carousel__slide"));
    const dotsWrap = root.querySelector("[data-carousel-dots]");
    const prev = root.querySelector("[data-carousel-prev]");
    const next = root.querySelector("[data-carousel-next]");
    if (!slides.length) return;

    let index = Math.max(
      0,
      slides.findIndex((s) => s.classList.contains("is-active"))
    );

    const dots = slides.map((_, i) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "carousel__dot";
      btn.setAttribute("aria-label", `Ir a la foto ${i + 1}`);
      btn.addEventListener("click", () => go(i));
      dotsWrap?.appendChild(btn);
      return btn;
    });

    const go = (i) => {
      index = (i + slides.length) % slides.length;
      slides.forEach((slide, n) => {
        slide.classList.toggle("is-active", n === index);
      });
      dots.forEach((dot, n) => {
        dot.classList.toggle("is-active", n === index);
      });
    };

    prev?.addEventListener("click", () => go(index - 1));
    next?.addEventListener("click", () => go(index + 1));

    root.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") go(index - 1);
      if (e.key === "ArrowRight") go(index + 1);
    });

    go(index);
  });

  const lightbox = document.querySelector("[data-lightbox]");
  const lightboxImg = document.querySelector("[data-lightbox-img]");
  const lightboxCap = document.querySelector("[data-lightbox-cap]");
  const thumbs = Array.from(document.querySelectorAll("[data-lightbox-gallery] .vision-thumb"));

  if (lightbox && lightboxImg && thumbs.length) {
    let lbIndex = 0;

    const openLb = (i) => {
      lbIndex = (i + thumbs.length) % thumbs.length;
      const thumb = thumbs[lbIndex];
      lightboxImg.src = thumb.dataset.full || "";
      lightboxImg.alt = thumb.dataset.caption || "";
      if (lightboxCap) lightboxCap.textContent = thumb.dataset.caption || "";
      lightbox.hidden = false;
      document.body.style.overflow = "hidden";
    };

    const closeLb = () => {
      lightbox.hidden = true;
      lightboxImg.removeAttribute("src");
      document.body.style.overflow = "";
    };

    thumbs.forEach((thumb, i) => {
      thumb.addEventListener("click", () => openLb(i));
    });

    lightbox.querySelector("[data-lightbox-close]")?.addEventListener("click", closeLb);
    lightbox.querySelector("[data-lightbox-prev]")?.addEventListener("click", () => openLb(lbIndex - 1));
    lightbox.querySelector("[data-lightbox-next]")?.addEventListener("click", () => openLb(lbIndex + 1));

    lightbox.addEventListener("click", (e) => {
      if (e.target === lightbox) closeLb();
    });

    document.addEventListener("keydown", (e) => {
      if (lightbox.hidden) return;
      if (e.key === "Escape") closeLb();
      if (e.key === "ArrowLeft") openLb(lbIndex - 1);
      if (e.key === "ArrowRight") openLb(lbIndex + 1);
    });
  }

  document.querySelectorAll("[data-pueblo-more]").forEach((btn) => {
    const prose = btn.previousElementSibling;
    if (!prose || !prose.hasAttribute("data-pueblo-fold")) return;

    btn.addEventListener("click", () => {
      const open = prose.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", String(open));
      btn.textContent = open ? "Ver menos" : "Seguir leyendo";
    });
  });
})();
