// Menu Hamburguesa
class Navigation {
  constructor() {
    this.toggle = document.getElementById('menu-toggle');
    this.nav = document.getElementById('nav');
    this.init();
  }

  init() {
    if (this.toggle && this.nav) {
      this.toggle.addEventListener('click', () => this.toggleMenu());
      
      // Cerrar menú al hacer clic en un enlace
      this.nav.addEventListener('click', (e) => {
        if (e.target.tagName === 'A') {
          this.closeMenu();
        }
      });

      // Cerrar menú al hacer clic fuera
      document.addEventListener('click', (e) => {
        if (!this.nav.contains(e.target) && !this.toggle.contains(e.target)) {
          this.closeMenu();
        }
      });
    }
  }

  toggleMenu() {
    this.nav.classList.toggle('show');
    this.toggle.classList.toggle('active');
  }

  closeMenu() {
    this.nav.classList.remove('show');
    this.toggle.classList.remove('active');
  }
}

// Transiciones entre páginas
class PageTransitions {
  constructor() {
    this.init();
  }

  init() {
    this.setupLinkInterceptions();
  }

  setupLinkInterceptions() {
    const links = document.querySelectorAll('a[href]');
    
    links.forEach(link => {
      // Solo interceptar enlaces internos
      if (this.isInternalLink(link)) {
        link.addEventListener('click', (e) => this.handleLinkClick(e, link));
      }
    });
  }

  isInternalLink(link) {
    return link.hostname === window.location.hostname && 
           !link.target && 
           link.getAttribute('href').startsWith('/') || 
           !link.getAttribute('href').includes('://');
  }

  handleLinkClick(e, link) {
    e.preventDefault();
    
    // Aplicar fade out
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.4s ease';
    
    // Navegar después de la animación
    setTimeout(() => {
      window.location.href = link.href;
    }, 400);
  }
}

// Mapa de Google
class FlowerMap {
  constructor() {
    if (typeof google !== 'undefined') {
      this.init();
    }
  }

  init() {
    const mapCenter = { lat: 19.4326, lng: -99.1332 };
    const map = new google.maps.Map(document.getElementById('map'), {
      zoom: 6,
      center: mapCenter,
      styles: this.getMapStyles(),
      gestureHandling: 'cooperative'
    });

    this.addFlowerZones(map);
  }

  getMapStyles() {
    return [
      {
        elementType: 'geometry',
        stylers: [{ color: '#f8f0f2' }]
      },
      {
        elementType: 'labels.text.fill',
        stylers: [{ color: '#444' }]
      },
      {
        featureType: 'water',
        stylers: [{ color: '#cde6e9' }]
      },
      {
        featureType: 'landscape',
        stylers: [{ color: '#f6e6e9' }]
      },
      {
        featureType: 'poi',
        stylers: [{ visibility: 'off' }]
      }
    ];
  }

  addFlowerZones(map) {
    const zones = [
      { 
        name: 'Valle de Bravo', 
        position: { lat: 19.195, lng: -100.13 },
        description: 'Zona de floración primaveral con especies nativas'
      },
      { 
        name: 'Puebla', 
        position: { lat: 19.04, lng: -98.2 },
        description: 'Región con diversidad floral todo el año'
      },
      { 
        name: 'Chiapas', 
        position: { lat: 16.75, lng: -93.12 },
        description: 'Área tropical con floración perenne'
      }
    ];

    zones.forEach(zone => {
      const marker = new google.maps.Marker({
        position: zone.position,
        map: map,
        title: zone.name,
        icon: {
          path: google.maps.SymbolPath.CIRCLE,
          fillColor: '#c05664',
          fillOpacity: 0.8,
          strokeColor: '#ffffff',
          strokeWeight: 2,
          scale: 10
        }
      });

      const infowindow = new google.maps.InfoWindow({
        content: `
          <div class="map-info-window">
            <h3>${zone.name}</h3>
            <p>${zone.description}</p>
            <small>Estado de floración: Activa</small>
          </div>
        `
      });

      marker.addListener('click', () => {
        infowindow.open(map, marker);
      });
    });
  }
}

// Manejo de formulario de contacto
class ContactForm {
  constructor() {
    this.form = document.querySelector('.contact-form');
    if (this.form) {
      this.init();
    }
  }

  init() {
    this.form.addEventListener('submit', (e) => this.handleSubmit(e));
  }

  handleSubmit(e) {
    e.preventDefault();
    
    // Validación básica
    const inputs = this.form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;

    inputs.forEach(input => {
      if (!input.value.trim()) {
        isValid = false;
        this.showError(input, 'Este campo es requerido');
      } else {
        this.clearError(input);
      }
    });

    if (isValid) {
      this.submitForm();
    }
  }

  showError(input, message) {
    this.clearError(input);
    
    const error = document.createElement('div');
    error.className = 'error-message';
    error.textContent = message;
    error.style.cssText = 'color: #c05664; font-size: 0.875rem; margin-top: 0.25rem;';
    
    input.parentNode.appendChild(error);
    input.style.borderColor = '#c05664';
  }

  clearError(input) {
    const existingError = input.parentNode.querySelector('.error-message');
    if (existingError) {
      existingError.remove();
    }
    input.style.borderColor = '';
  }

  submitForm() {
    const submitBtn = this.form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    submitBtn.textContent = 'Enviando...';
    submitBtn.disabled = true;

    // Simular envío (en un caso real, aquí iría una petición AJAX)
    setTimeout(() => {
      alert('Mensaje enviado correctamente. Te contactaremos pronto.');
      this.form.reset();
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    }, 1500);
  }
}

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
  new Navigation();
  new PageTransitions();
  new ContactForm();

  // Inicializar mapa si la función global existe
  if (typeof iniciarMapa !== 'undefined') {
    window.iniciarMapa = () => new FlowerMap();
  }
});

// Restaurar opacidad al cargar nueva página
window.addEventListener('pageshow', function() {
  document.body.style.opacity = '1';
});