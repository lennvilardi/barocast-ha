class LocalWeatherForecastCard extends HTMLElement {
  static getStubConfig() {
    return {
      entity: "sensor.local_forecast",
      detail_entity: "sensor.local_forecast_zambretti_detail",
      pressure_change_entity: "sensor.local_forecast_pressurechange",
      icon_now: "mdi:weather-cloudy-clock"
    };
  }

  setConfig(config) {
    if (!config || !config.entity) {
      throw new Error("You need to define an entity (e.g. sensor.local_forecast)");
    }
    this._config = {
      detail_entity: "sensor.local_forecast_zambretti_detail",
      pressure_change_entity: "sensor.local_forecast_pressurechange",
      icon_now: "mdi:weather-cloudy-clock",
      ...config
    };

    if (!this.shadowRoot) {
      this.attachShadow({ mode: "open" });
    }
  }

  _labels(langIndex) {
    // Language index is produced by the integration:
    // 0=de, 1=en, 2=el, 3=it, 4=fr
    const labels = {
      now: ["Jetzt", "Now", "Τώρα", "Adesso", "Maintenant"],
      forecast: ["Vorhersage", "Forecast", "Πρόγνωση", "Previsioni", "Prévisions"],
      pressure: ["Druck", "Pressure", "Πίεση", "Pressione", "Pression"],
      rain: ["Regen", "Rain", "Βροχή", "Pioggia", "Pluie"],
      in3h: ["in 3 Std.", "in 3h", "σε 3 ώρες", "nelle prossime 3h", "en 3h"],
      unavailable: ["Nicht verfügbar", "Unavailable", "Μη διαθέσιμο", "Non disponibile", "Indisponible"]
    };

    const idx = Number.isInteger(langIndex) ? Math.max(0, Math.min(4, langIndex)) : 1;
    return {
      now: labels.now[idx],
      forecast: labels.forecast[idx],
      pressure: labels.pressure[idx],
      rain: labels.rain[idx],
      in3h: labels.in3h[idx],
      unavailable: labels.unavailable[idx]
    };
  }

  _safeArray(value, fallback = []) {
    return Array.isArray(value) ? value : fallback;
  }

  _formatTemp(value) {
    if (value === undefined || value === null || value === "unavailable") return "-";
    const num = Number(value);
    if (Number.isNaN(num)) return "-";
    return `${num.toFixed(1)}°C`;
  }

  set hass(hass) {
    if (!this._config || !hass) return;

    // Read entities produced by the integration. The card stays defensive and
    // degrades gracefully when Home Assistant is still starting up.
    const main = hass.states[this._config.entity];
    const detail = hass.states[this._config.detail_entity];
    const pressureChange = hass.states[this._config.pressure_change_entity];

    const langRaw = Number(main?.attributes?.language ?? 1);
    const langIndex = Number.isInteger(langRaw) ? Math.max(0, Math.min(4, langRaw)) : 1;
    const L = this._labels(langIndex);

    const title = main?.state ?? "Local Weather Forecast";
    const shortTerm = this._safeArray(main?.attributes?.forecast_short_term, []);
    const shortText = shortTerm[0] ?? L.unavailable;

    const forecast = this._safeArray(main?.attributes?.forecast_zambretti, []);
    const forecastText = forecast[0] ?? L.unavailable;

    const trend = this._safeArray(main?.attributes?.forecast_pressure_trend, []);
    const trendText = trend[0] ?? "-";

    const temps = this._safeArray(main?.attributes?.forecast_temp_short, []);
    const tempAtSlot = Number(temps[1]);
    const nextTemp = temps[0];

    const currentTemp = this._formatTemp(main?.attributes?.temperature);

    const rain = this._safeArray(detail?.attributes?.rain_prob, [0, 0]);
    const icons = this._safeArray(detail?.attributes?.icons, ["mdi:weather-cloudy", "mdi:weather-cloudy"]);
    const t1 = this._safeArray(detail?.attributes?.first_time, ["--:--", 0]);
    const t2 = this._safeArray(detail?.attributes?.second_time, ["--:--", 0]);

    const slot1Temp = tempAtSlot === 0 ? this._formatTemp(nextTemp) : "-";
    const slot2Temp = tempAtSlot === 1 ? this._formatTemp(nextTemp) : "-";

    const pressureValue = pressureChange?.state ?? main?.attributes?.pressure_change_3h ?? "-";

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
        }
        ha-card {
          position: relative;
          overflow: hidden;
          border-radius: 18px;
          padding: 14px;
          color: var(--primary-text-color);
          background:
            radial-gradient(120% 90% at 0% 0%, rgba(67, 123, 255, 0.14), transparent 55%),
            radial-gradient(100% 120% at 100% 100%, rgba(36, 177, 116, 0.14), transparent 62%),
            linear-gradient(140deg, var(--card-background-color), color-mix(in srgb, var(--card-background-color), #0b2740 8%));
        }
        .header {
          display: flex;
          justify-content: space-between;
          align-items: baseline;
          gap: 8px;
          margin-bottom: 12px;
        }
        .title {
          font-size: 1.1rem;
          font-weight: 700;
          line-height: 1.2;
        }
        .chip {
          font-size: 0.78rem;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          border-radius: 999px;
          padding: 5px 9px;
          background: color-mix(in srgb, var(--primary-color), transparent 82%);
          color: var(--primary-color);
        }
        .grid {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 10px;
          margin-bottom: 12px;
        }
        .cell {
          border-radius: 14px;
          padding: 10px;
          background: color-mix(in srgb, var(--card-background-color), var(--primary-text-color) 3%);
          border: 1px solid color-mix(in srgb, var(--divider-color), transparent 30%);
          min-height: 92px;
        }
        .cell-head {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 6px;
          font-size: 0.78rem;
          opacity: 0.9;
        }
        .icon {
          --mdc-icon-size: 22px;
          color: var(--primary-color);
        }
        .main {
          font-size: 0.98rem;
          font-weight: 600;
          line-height: 1.25;
          margin-bottom: 6px;
        }
        .meta {
          font-size: 0.82rem;
          line-height: 1.35;
          opacity: 0.9;
        }
        .footer {
          border-radius: 14px;
          padding: 10px;
          background: color-mix(in srgb, var(--card-background-color), var(--primary-text-color) 2%);
          border: 1px solid color-mix(in srgb, var(--divider-color), transparent 30%);
        }
        .footer .line {
          font-size: 0.88rem;
          line-height: 1.35;
          margin: 2px 0;
        }
      </style>

      <ha-card>
        <div class="header">
          <div class="title">${title}</div>
          <div class="chip">Zambretti</div>
        </div>

        <div class="grid">
          <div class="cell">
            <div class="cell-head">
              <span>${L.now}</span>
              <ha-icon class="icon" icon="${this._config.icon_now}"></ha-icon>
            </div>
            <div class="main">${shortText}</div>
            <div class="meta">${currentTemp}</div>
          </div>

          <div class="cell">
            <div class="cell-head">
              <span>~ ${t1[0]}</span>
              <ha-icon class="icon" icon="${icons[0]}"></ha-icon>
            </div>
            <div class="main">${L.rain}: ${rain[0]}%</div>
            <div class="meta">${slot1Temp}</div>
          </div>

          <div class="cell">
            <div class="cell-head">
              <span>~ ${t2[0]}</span>
              <ha-icon class="icon" icon="${icons[1]}"></ha-icon>
            </div>
            <div class="main">${L.rain}: ${rain[1]}%</div>
            <div class="meta">${slot2Temp}</div>
          </div>
        </div>

        <div class="footer">
          <div class="line"><strong>${L.forecast}:</strong> ${forecastText}</div>
          <div class="line"><strong>${L.pressure}:</strong> ${trendText}, ${pressureValue} hPa ${L.in3h}</div>
        </div>
      </ha-card>
    `;
  }

  getCardSize() {
    return 4;
  }
}

customElements.define("local-weather-forecast-card", LocalWeatherForecastCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "local-weather-forecast-card",
  name: "Local Weather Forecast Card",
  description: "A polished 12h local weather card for sensors from Local Weather Forecast integration"
});
