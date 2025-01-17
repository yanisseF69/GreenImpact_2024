/**
* Template Name: Bootslander
* Template URL: https://bootstrapmade.com/bootslander-free-bootstrap-landing-page-template/
* Updated: Mar 17 2024 with Bootstrap v5.3.3
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Scrolls to an element with header offset
   */
  const scrollto = (el) => {
    let header = select('#header')
    let offset = header.offsetHeight

    if (!header.classList.contains('header-scrolled')) {
      offset -= 20
    }

    let elementPos = select(el).offsetTop
    window.scrollTo({
      top: elementPos - offset,
      behavior: 'smooth'
    })
  }

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Mobile nav toggle
   */
  on('click', '.mobile-nav-toggle', function(e) {
    select('#navbar').classList.toggle('navbar-mobile')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  /**
   * Mobile nav dropdowns activate
   */
  on('click', '.navbar .dropdown > a', function(e) {
    if (select('#navbar').classList.contains('navbar-mobile')) {
      e.preventDefault()
      this.nextElementSibling.classList.toggle('dropdown-active')
    }
  }, true)

  /**
   * Scrool with ofset on links with a class name .scrollto
   */
  on('click', '.scrollto', function(e) {
    if (select(this.hash)) {
      e.preventDefault()

      let navbar = select('#navbar')
      if (navbar.classList.contains('navbar-mobile')) {
        navbar.classList.remove('navbar-mobile')
        let navbarToggle = select('.mobile-nav-toggle')
        navbarToggle.classList.toggle('bi-list')
        navbarToggle.classList.toggle('bi-x')
      }
      scrollto(this.hash)
    }
  }, true)

  /**
   * Scroll with ofset on page load with hash links in the url
   */
  window.addEventListener('load', () => {
    if (window.location.hash) {
      if (select(window.location.hash)) {
        scrollto(window.location.hash)
      }
    }
  });

  /**
   * Preloader
   */
  let preloader = select('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove()
    });
  }

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Initiate gallery lightbox 
   */
  const galleryLightbox = GLightbox({
    selector: '.gallery-lightbox'
  });

  /**
   * Testimonials slider
   */
  new Swiper('.testimonials-slider', {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    }
  });

  /**
   * Animation on scroll
   */
  window.addEventListener('load', () => {
    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    })
  });

  /**
   * Initiate Pure Counter 
   */
  new PureCounter();

})()

/**
 * Generate graphs
 */
function prepareDataForCharts(categoryData) {
  var chartData = {};
  Object.keys(categoryData).forEach(function(category) {
      chartData[category] = {
          labels: [],
          data: [],
          backgroundColor: [],
          borderColor: []
      };
      var colorPalette = [
        'rgba(52, 78, 65, 1)', // #344E41
        'rgba(58, 90, 64, 1)', // #3A5A40
        'rgba(88, 129, 87, 1)', // #588157
        'rgba(90, 159, 104, 1)', // #5A9F68
        'rgba(62, 130, 65, 1)', // #3E8241
        'rgba(187, 213, 142, 1)', // #BBD58E
        'rgba(75, 111, 68, 1)', // #4B6F44
        'rgba(101, 140, 89, 1)',// #658A59
        'rgba(130, 167, 102, 1)', // #82A766 
        'rgba(168, 192, 120, 1)', // #A8C078 
      ];

      categoryData[category].forEach(function(typage, index) {
          chartData[category].labels.push(typage[0]);
          chartData[category].data.push(typage[1]);
          chartData[category].backgroundColor.push(colorPalette[index % colorPalette.length]);
          chartData[category].borderColor.push(colorPalette[index % colorPalette.length]);
      });
  });
  return chartData;
}

/**
 * Generate graphs
 */

function generateCharts(categoryData) {
  var chartData = prepareDataForCharts(categoryData);
  Object.keys(chartData).forEach(function(category, index) {
      var canvasId = 'myChart' + (index + 1);
      var ctx = document.getElementById(canvasId).getContext('2d');
      var myChart = new Chart(ctx, {
          type: 'doughnut',
          data: {
              labels: chartData[category].labels,
              datasets: [{
                  label: 'Empreinte Carbone',
                  data: chartData[category].data,
                  backgroundColor: chartData[category].backgroundColor,
                  borderColor: chartData[category].borderColor,
                  borderWidth: 1
              }]
          },
          options: {
              scales: {
                  y: {
                      display: false
                  }
              },
              plugins: {
                  legend: {
                      display: true,
                      position: 'top'
                  }
              }
          }
      });
  });
}

function generateGlobalChartsResults(results) {
  var chartData = prepareDataForCharts(results);
  var canvasId = 'myGlobalResultChart'; 
  var ctx = document.getElementById(canvasId).getContext('2d');
  
  var mergedLabels = [];
  var mergedData = [];
  var mergedBackgroundColor = [];
  var mergedBorderColor = [];

  var colorPalette = [
    'rgba(52, 78, 65, 1)', // #344E41
    'rgba(58, 90, 64, 1)', // #3A5A40
    'rgba(88, 129, 87, 1)', // #588157
    'rgba(90, 159, 104, 1)', // #5A9F68
    'rgba(62, 130, 65, 1)', // #3E8241
    'rgba(187, 213, 142, 1)', // #BBD58E
    'rgba(75, 111, 68, 1)', // #4B6F44
    'rgba(101, 140, 89, 1)',// #658A59
    'rgba(130, 167, 102, 1)', // #82A766 
    'rgba(168, 192, 120, 1)', // #A8C078 
  ];

  var paletteIndex = 0;

  Object.keys(chartData).forEach(function(category) {
    mergedLabels = mergedLabels.concat(chartData[category].labels);
    mergedData = mergedData.concat(chartData[category].data);

    var categoryBackgroundColor = [];
    var categoryBorderColor = [];

    chartData[category].labels.forEach(function(label, index) {
      categoryBackgroundColor.push(colorPalette[paletteIndex]);
      categoryBorderColor.push(colorPalette[paletteIndex]);
      paletteIndex = (paletteIndex + 1) % colorPalette.length; 
    });

    mergedBackgroundColor = mergedBackgroundColor.concat(categoryBackgroundColor);
    mergedBorderColor = mergedBorderColor.concat(categoryBorderColor);
  });

  var myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: mergedLabels,
      datasets: [{
        label: 'Votre Empreinte Carbone',
        data: mergedData,
        backgroundColor: mergedBackgroundColor,
        borderColor: mergedBorderColor,
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          display: false
        }
      },
      plugins: {
        legend: {
          display: true,
          position: 'top'
        }
      }
    }
  });
}

function generateChartsResults(result_data) {
  var canvasId = 'myResultChart';
  var ctx = document.getElementById(canvasId).getContext('2d');
  var colorPalette = [
    'rgba(52, 78, 65, 1)', // #344E41
    'rgba(58, 90, 64, 1)', // #3A5A40
    'rgba(88, 129, 87, 1)', // #588157
    'rgba(90, 159, 104, 1)', // #5A9F68
    'rgba(62, 130, 65, 1)', // #3E8241
    'rgba(187, 213, 142, 1)', // #BBD58E
    'rgba(75, 111, 68, 1)', // #4B6F44
    'rgba(101, 140, 89, 1)',// #658A59
    'rgba(130, 167, 102, 1)', // #82A766 
    'rgba(168, 192, 120, 1)', // #A8C078 
  ];
  var labels = Object.keys(result_data); 
  var data = Object.values(result_data); 
  var myChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
          labels: labels, 
          datasets: [{
              label: 'Empreinte Carbone',
              data: data, 
              backgroundColor: colorPalette.slice(0, labels.length),
              borderColor: colorPalette.slice(0, labels.length),
              borderWidth: 2
          }]
      },
      options: {
          plugins: {
              legend: {
                  display: true,
                  position: 'top'
              }
          }
      }
  });

}


document.addEventListener('DOMContentLoaded', function() {
  fetch('/get_category_avg_carbon_footprint')
      .then(response => response.json())
      .then(categoryData => {
          generateCharts(categoryData);
      })
      .catch(error => console.error('Erreur lors de la récupération des données:', error));
});

document.addEventListener('DOMContentLoaded', function() {
  generateChartsResults(results);
});

document.addEventListener('DOMContentLoaded', function() {
  fetch('/get_avg_carbon_footprint')
      .then(response => response.json())
      .then(categoryData => {
        generateGlobalChartsResults(categoryData);
      })
      .catch(error => console.error('Erreur lors de la récupération des données:', error));
});