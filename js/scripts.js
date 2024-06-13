// Crear el mapa
var map = L.map('map', {
    center: [39.9,-3.1],
    zoom: 7,
    fullscreenControl: true,
    fullscreenControlOptions: {
        position: 'topleft'
    }
});

// Añadir capas de fondo
var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 20,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">Colaboradores de OpenStreetMap</a>'
}).addTo(map);

var osm2 = new L.TileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
    minZoom: 0,
    maxZoom: 13,
    attribution: "Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL."
});

const serveiOrtoCache = L.tileLayer.wms("https://geoserveis.icgc.cat/icc_mapesmultibase/utm/wms/service?", {
    layers: 'orto',
    format: 'image/jpeg',
    continuousWorld: true,
    attribution: 'Institut Cartogràfic i Geològic de Catalunya',
});

// Añadir capas WMS y WFS a partir de petición a GeoServer
var secciones = L.tileLayer.betterWms("http://localhost:8082/geoserver/TFM/wms?service=WMS", {
    layers: 'comercios_poblacion_view',
    format: 'image/png',
    transparent: true,
    crs: L.CRS.EPSG4326,
    proxy: 'lib/php/proxy.php',
    proxyParamName: 'site'
}).addTo(map);

var owsrootUrl = 'http://localhost:8082/geoserver/TFM/ows';

var defaultParameters = {
    service: 'WFS',
    version: '1.0.0',
    request: 'GetFeature',
    typeName: 'TFM:comercios',
    outputFormat: 'application/json'
};

var parameters = L.Util.extend(defaultParameters);

var URL = owsrootUrl + L.Util.getParamString(parameters);

var iconMap = {
    bakery: "https://wiki.openstreetmap.org/w/images/f/fe/Bakery-16.svg",
    bar: "https://wiki.openstreetmap.org/w/images/9/94/Bar-16.svg",
    butcher: "https://wiki.openstreetmap.org/w/images/b/b8/Butcher.svg",
    cafe: "https://wiki.openstreetmap.org/w/images/d/da/Cafe-16.svg",
    convenience: "https://wiki.openstreetmap.org/w/images/9/96/Convenience-14.svg",
    fast_food: "https://wiki.openstreetmap.org/w/images/1/1f/Fast-food-16.svg",
    frozen_food: "https://wiki.openstreetmap.org/w/images/d/db/FrozenFood_symbol.svg",
    greengrocer: "https://wiki.openstreetmap.org/w/images/d/d8/Greengrocer-14.svg",
    marketplace: "https://wiki.openstreetmap.org/w/images/1/1c/Marketplace-14.svg",
    pastry: "https://wiki.openstreetmap.org/w/images/c/cc/Confectionery-14.svg",
    restaurant: "https://wiki.openstreetmap.org/w/images/b/bb/Restaurant-14.svg",
    seafood: "https://wiki.openstreetmap.org/w/images/d/d9/Seafood-14.svg",
    supermarket: "https://wiki.openstreetmap.org/w/images/7/76/Supermarket-14.svg"
};

function getPopupContent(feature) {
    return `
        <b>KEY:</b> ${feature.properties.key}<br>
        <b>TYPE:</b> ${feature.properties.type}<br>
        <b>NOMBRE:</b> ${feature.properties.name}<br>
        <b>COORD.:</b> ${feature.properties.lat}, ${feature.properties.lon}
    `;
}

$.ajax({
    url: URL,
    success: function (data) {
        var comercios = new L.geoJson(data, {
            pointToLayer: function (feature, latlng) {
                var type = feature.properties.type;
                var iconUrl = iconMap[type]
                var icon = L.icon({
                    iconUrl: iconUrl,
                    iconSize: [18, 18],
                    iconAnchor: [9, 9],
                    popupAnchor: [0, -10]
                });
                return L.marker(latlng, { icon: icon });
            },
            onEachFeature: function (feature, layer) {
                layer.bindPopup(getPopupContent(feature));
            }
        });

        // Ajustar la vista del mapa a la extensión de la capa "comercios"
        var bounds = comercios.getBounds();
        var center = bounds.getCenter();
        // map.fitBounds(comercios.getBounds()); <--- Alternativa (no se comporta igual, falla)
        
        overlays["Comercios (WFS)"] = comercios;
        layerControl.addOverlay(comercios, "Comercios (WFS)");

        map.setView(center, 12);

    }
});

// Añadir funcionalidades adicionales
var miniMap = new L.Control.MiniMap(osm2).addTo(map);

L.control.mousePosition().addTo(map);

L.control.scale({
    position: 'bottomleft',
    imperial: false
}).addTo(map);

// Definir las capas en el control de capas
const baseMaps = {
    "Base (OSM)": osm,
    "Ortofoto (ICGC)": serveiOrtoCache,
};

const overlays = {
    "Secciones (WMS)": secciones,
};

var layerControl = L.control.layers(baseMaps, overlays).addTo(map);

// Añadir leyendas
var legend_comercios = L.control({ position: 'bottomleft' });
legend_comercios.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend');
    div.innerHTML += '<div class="legend-container"><h4>Comercios:</h4><img src="http://localhost:8082/geoserver/TFM/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=comercios" alt="Legend"></div>';
    return div;
};

var legend_secciones = L.control({ position: 'bottomleft' });
legend_secciones.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'legend');
    div.innerHTML += '<div class="legend-container"><h4>Número de comercios <br>por cada 100 habitantes:</h4><img src="http://localhost:8082/geoserver/TFM/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=comercios_poblacion_view" alt="Legend"></div>';
    return div;
};

legend_secciones.addTo(map);
legend_comercios.addTo(map);