document.addEventListener('DOMContentLoaded', () => {
  // toggle edit profile form
  const editBtn = document.getElementById('edit-btn');
  const form = document.getElementById('profile-form');
  if (editBtn && form) {
    editBtn.addEventListener('click', () => {
      form.classList.toggle('hidden');
    });
  }

  // toggle description
  const toggleBtn = document.getElementById('toggle-description');
  const descContent = document.getElementById('description-content');
  if (toggleBtn && descContent) {
    toggleBtn.addEventListener('click', () => {
      descContent.classList.toggle('hidden');
      toggleBtn.textContent = descContent.classList.contains('hidden') ? 'Show' : 'Hide';
    });
  }

  // Swiper for image slideshow
  if (typeof Swiper !== 'undefined') {
    new Swiper(".mySwiper", {
      slidesPerView: 3,
      loop: true,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev"
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true
      }
    });
  }

  // fallback for broken img urls
  const placeholders = [
    "/static/images/placeholder1.jpg",
    "/static/images/placeholder2.jpg",
    "/static/images/placeholder3.jpg",
    "/static/images/placeholder4.jpg",
    "/static/images/placeholder5.jpg"
  ];

  let placeholderIndex = 0;

  document.querySelectorAll('img').forEach(img => {
    img.onerror = () => {
      if (!img.src.includes('placeholder')) {
        img.src = placeholders[placeholderIndex % placeholders.length];
        placeholderIndex++;
      }
    };
  });
});

// modal image viewer
function openModal(imageUrl) {
  const modal = document.getElementById("imageModal");
  const modalImg = document.getElementById("modalImage");
  modalImg.src = imageUrl;
  modal.classList.remove("hidden");
  modal.classList.add("flex");
}

function closeModal() {
  const modal = document.getElementById("imageModal");
  modal.classList.remove("flex");
  modal.classList.add("hidden");
}