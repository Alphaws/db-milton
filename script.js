(function () {
  'use strict';

  var root = document.documentElement;
  var chapterLinks = Array.from(document.querySelectorAll('[data-chapter-link]'));
  var slides = Array.from(document.querySelectorAll('.slide'));
  var prevBtn = document.getElementById('prevSlide');
  var nextBtn = document.getElementById('nextSlide');
  var slideCounter = document.getElementById('slideCounter');
  var scrollMeter = document.getElementById('scrollMeter');
  
  var currentSlideIndex = 0;
  root.classList.add('js-enabled');

  function updateSlide(index) {
    if (index < 0) index = 0;
    if (index >= slides.length) index = slides.length - 1;
    currentSlideIndex = index;

    slides.forEach(function (slide, i) {
      slide.classList.toggle('active', i === index);
    });

    chapterLinks.forEach(function (link, i) {
      link.classList.toggle('is-active', i === index);
      if (i === index) {
        link.setAttribute('aria-current', 'step');
        link.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      } else {
        link.removeAttribute('aria-current');
      }
    });

    if (slideCounter) {
      slideCounter.textContent = (currentSlideIndex + 1).toString().padStart(2, '0') + ' / ' + slides.length.toString().padStart(2, '0');
    }

    if (scrollMeter) {
      var progress = ((currentSlideIndex + 1) / slides.length) * 100;
      scrollMeter.style.width = progress + '%';
    }

    // Scroll to top of current slide container
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Gomb eseménykezelők
  if (prevBtn) {
    prevBtn.addEventListener('click', function () {
      updateSlide(currentSlideIndex - 1);
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', function () {
      updateSlide(currentSlideIndex + 1);
    });
  }

  // Billentyűzet navigáció: Balra / Jobbra / Space / PageUp / PageDown
  window.addEventListener('keydown', function (e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
      e.preventDefault();
      updateSlide(currentSlideIndex + 1);
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
      e.preventDefault();
      updateSlide(currentSlideIndex - 1);
    }
  });

  // Navigációs linkek kattintása
  chapterLinks.forEach(function (link, i) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      updateSlide(i);
    });
  });

  // Másolás vágólapra kódblokkokhoz
  document.querySelectorAll('.copy-btn').forEach(function (button) {
    button.addEventListener('click', function () {
      var code = this.closest('.code-card').querySelector('code').innerText;
      navigator.clipboard.writeText(code).then(function () {
        var orig = button.textContent;
        button.textContent = 'Másolva!';
        setTimeout(function () { button.textContent = orig; }, 1800);
      });
    });
  });

  // SQL Végrehajtó Motor (API Hívás)
  function executeSQLQuery(sqlText, targetResultContainer, triggerButton) {
    if (!sqlText || !sqlText.trim()) return;
    
    var origText = triggerButton ? triggerButton.textContent : '';
    if (triggerButton) {
      triggerButton.textContent = '⏳ Fut...';
      triggerButton.disabled = true;
    }

    targetResultContainer.classList.add('has-result');
    targetResultContainer.innerHTML = '<div style="color: var(--teal-light); font-family: var(--mono); font-size: 0.8rem; padding: 0.5rem 0;">⏳ Lekérdezés futtatása MariaDB-ben...</div>';

    fetch('/api/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sql: sqlText })
    })
    .then(function (res) { return res.json(); })
    .then(function (data) {
      if (triggerButton) {
        triggerButton.textContent = origText;
        triggerButton.disabled = false;
      }

      if (data.error) {
        targetResultContainer.innerHTML = '<div style="color: #f87171; font-family: var(--mono); font-size: 0.8rem; padding: 0.4rem 0;">❌ Hiba: ' + escapeHtml(data.error) + '</div>';
        return;
      }

      if (data.affected) {
        targetResultContainer.innerHTML = '<div style="color: #34d399; font-family: var(--mono); font-size: 0.8rem; padding: 0.4rem 0;">✓ ' + escapeHtml(data.affected) + '</div>';
        return;
      }

      // Táblázat renderelése
      var html = '<div style="margin-bottom: 0.6rem; display: flex; justify-content: space-between; font-family: var(--mono); font-size: 0.85rem; color: var(--teal-light); font-weight: 600;">' +
                 '<span>✓ Eredmény halmaz (' + data.count + ' sor)</span>' +
                 '<span style="color: var(--text-muted); font-size: 0.78rem;">MariaDB 11.4 OK</span></div>';
      
      html += '<div class="data-table-wrap" style="margin: 0; max-height: none; overflow: visible;"><table class="data-table" style="font-size: 0.9rem;"><thead><tr>';
      data.columns.forEach(function (col) {
        html += '<th style="padding: 0.85rem 1.1rem; font-size: 0.85rem;">' + escapeHtml(col) + '</th>';
      });
      html += '</tr></thead><tbody>';

      if (data.rows.length === 0) {
        html += '<tr><td colspan="' + data.columns.length + '" style="text-align: center; color: var(--text-muted); padding: 1rem;">Üres eredmény.</td></tr>';
      } else {
        data.rows.forEach(function (row) {
          html += '<tr>';
          row.forEach(function (cell) {
            html += '<td style="padding: 0.75rem 1.1rem; font-size: 0.88rem;">' + escapeHtml(cell !== null ? cell : 'NULL') + '</td>';
          });
          html += '</tr>';
        });
      }
      html += '</tbody></table></div>';
      targetResultContainer.innerHTML = html;
    })
    .catch(function (err) {
      if (triggerButton) {
        triggerButton.textContent = origText;
        triggerButton.disabled = false;
      }
      targetResultContainer.innerHTML = '<div style="color: #f87171; font-family: var(--mono); font-size: 0.8rem;">❌ Hálózati hiba: ' + escapeHtml(err.message) + '</div>';
    });
  }

  function escapeHtml(str) {
    if (typeof str !== 'string') return str;
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // Előre megírt SQL kártyák Futtatás gombja
  document.querySelectorAll('.run-card-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var card = this.closest('.code-card');
      var sql = card.querySelector('code').innerText;
      var resultBox = card.querySelector('.query-result-box');
      executeSQLQuery(sql, resultBox, this);
    });
  });

  // Interaktív Konzol SQL futtató gombja
  var customRunBtn = document.getElementById('runCustomQueryBtn');
  var customSqlArea = document.getElementById('customSqlText');
  var customResultBox = document.getElementById('customQueryResultBox');
  var presetSelect = document.getElementById('sqlPresetSelect');
  var resetDbBtn = document.getElementById('resetDatabaseBtn');

  if (resetDbBtn && customResultBox) {
    resetDbBtn.addEventListener('click', function () {
      if (!confirm('Biztosan visszaállítod a teljes adatbázist az eredeti állapotra? (Minden tábla újralétrejön és az eredeti mintarekordok töltődnek vissza)')) {
        return;
      }
      var btn = this;
      var origText = btn.textContent;
      btn.textContent = '⏳ Visszaállítás...';
      btn.disabled = true;

      customResultBox.classList.add('has-result');
      customResultBox.innerHTML = '<div style="color: var(--teal-light); font-family: var(--mono); font-size: 0.8rem; padding: 0.5rem 0;">⏳ Adatbázis újraépítése folyamatban...</div>';

      fetch('/api/reset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        btn.textContent = origText;
        btn.disabled = false;
        if (data.error) {
          customResultBox.innerHTML = '<div style="color: #f87171; font-family: var(--mono); font-size: 0.8rem;">❌ Hiba: ' + escapeHtml(data.error) + '</div>';
        } else {
          customResultBox.innerHTML = '<div style="color: #34d399; font-family: var(--mono); font-size: 0.85rem; padding: 0.5rem 0;">✅ ' + escapeHtml(data.message) + '</div>';
        }
      })
      .catch(function (err) {
        btn.textContent = origText;
        btn.disabled = false;
        customResultBox.innerHTML = '<div style="color: #f87171; font-family: var(--mono); font-size: 0.8rem;">❌ Hiba történt: ' + escapeHtml(err.message) + '</div>';
      });
    });
  }

  if (customRunBtn && customSqlArea && customResultBox) {
    customRunBtn.addEventListener('click', function () {
      executeSQLQuery(customSqlArea.value, customResultBox, this);
    });
  }

  if (presetSelect && customSqlArea) {
    presetSelect.addEventListener('change', function () {
      if (this.value) {
        customSqlArea.value = this.value;
      }
    });
  }

  // Kezdőállapot
  updateSlide(0);

})();
