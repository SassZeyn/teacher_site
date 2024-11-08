

// Function to toggle mobile navigation menu
// Function to toggle mobile navigation menu
// Function to toggle mobile navigation menu
// Function to toggle mobile navigation menu
// Function to toggle mobile navigation menu based on screen width
// Set the desired screen width threshold for the hamburger menu to activate
// Set the screen width threshold for the hamburger menu to activate
// Set the screen width threshold for the hamburger menu to activate
const HAMBURGER_THRESHOLD = 1300;

// Function to toggle mobile navigation menu based on screen width
function toggleMenu() {
    const menu = document.getElementById('nav-menu');
    const screenWidth = window.innerWidth;

    // Check if screen width is less than or equal to the threshold
    if (screenWidth <= HAMBURGER_THRESHOLD) {
        const isActive = menu.classList.toggle('active');

        // If the menu is being opened, add a click event listener to close it when clicking outside
        if (isActive) {
            document.addEventListener('click', handleOutsideClick);
        } else {
            document.removeEventListener('click', handleOutsideClick);
        }
    }
}

// Function to handle clicks outside the menu
function handleOutsideClick(event) {
    const menu = document.getElementById('nav-menu');
    const toggle = document.querySelector('.menu-toggle');

    // Check if the click is outside the menu and the toggle button
    if (!menu.contains(event.target) && !toggle.contains(event.target)) {
        menu.classList.remove('active');
        document.removeEventListener('click', handleOutsideClick); // Remove the event listener once closed
    }
}

// Close the menu if resizing from mobile to desktop view
window.addEventListener('resize', () => {
    const menu = document.getElementById('nav-menu');
    const screenWidth = window.innerWidth;

    // Close the menu if screen is resized to a width above the threshold
    if (screenWidth > HAMBURGER_THRESHOLD && menu.classList.contains('active')) {
        menu.classList.remove('active');
        document.removeEventListener('click', handleOutsideClick);
    }
});








// Swiper.js initialization for the video slider
// Swiper.js initialization for the video slider
// Swiper.js initialization for the video slider
document.addEventListener('DOMContentLoaded', function () {
    var swiper = new Swiper('.top-watch-swiper', {
        slidesPerView: 3, // Number of videos visible at a time
        spaceBetween: 30, // Space between video cards
        centeredSlides: false,
        autoplay: {
            delay: 3000, // Auto-slide every 3 seconds
            disableOnInteraction: false,
        },
        pagination: {
            el: '.top-watch-swiper .swiper-pagination',
            clickable: true,
        },
        breakpoints: {
            640: { slidesPerView: 1 },
            768: { slidesPerView: 2 },
            1024: { slidesPerView: 3 }
        },
        // Enable touch control for swipe/drag functionality
        simulateTouch: true,
        grabCursor: true, // Show a "grab" cursor for desktop
    });
});






// SweetAlert2 popup for booking success
function showBookingSuccessPopup() {
    Swal.fire({
        title: 'Booking Successful!',
        text: 'Your lesson is pending confirmation.',
        icon: 'success',
        confirmButtonText: 'OK'
    });
}

// Remove Flatpickr Initialization (handled by Calendly widget)

// Remove form submission logic for adding Google Calendar Event
// Since Calendly will handle scheduling, the manual date management is no longer needed

// Show a confirmation message after booking form submission (handled by Calendly)
document.querySelector(".booking-form").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevents the form from being submitted

    // For the Calendly widget, no need to send the form data manually.
    // The success popup can be triggered after successful booking via Calendly
    showBookingSuccessPopup();
});

// Add scroll event listener to window
window.addEventListener('scroll', function () {
    const navbar = document.querySelector('.navbar');
    const links = document.querySelectorAll('.navbar ul li a');

    // Check if the window has been scrolled more than 50px from the top
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled'); // Add class when scrolled
        links.forEach(link => link.classList.remove('transparent')); // Remove transparent class
    } else {
        navbar.classList.remove('scrolled'); // Remove class when at the top
        links.forEach(link => link.classList.add('transparent')); // Add transparent class
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const backToTopButton = document.querySelector('.back-to-top');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTopButton.classList.add('show');
        } else {
            backToTopButton.classList.remove('show');
        }
    });
});

