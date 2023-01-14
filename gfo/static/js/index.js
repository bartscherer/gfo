var CONVERTED_URLS = [];
var DOWNLOADED_URLS = [];

const element = (elementID) => {
    return document.getElementById(elementID);
}

const isValidURL = (urlString) => {
    let url;
    try
    {
        url = new URL(urlString);
    }
    catch(_)
    {
        return false;
    }
    return ['http:', 'https:'].indexOf(url.protocol) !== -1;
}

const validateURLOnInput = (evt) => {
    let url = evt.target.value.toLowerCase();
    let urlInput = element('urlInput');
    if(url.length === 0)
    {
        clearURLInput();
        return false;
    }
    if(url.split(':')[0] === 'http')
    {
        url = `https${url.substring(4, url.length)}`;
    }
    if(
        isValidURL(url) && 
        (
            url.indexOf('fonts.googleapis.com/css?') !== -1 ||
            url.indexOf('fonts.googleapis.com/css2?') !== -1
        )
    )
    {
        urlInput.classList.remove('input-invalid');
        urlInput.classList.add('input-valid');
        return true;
    }
    else
    {
        urlInput.classList.remove('input-valid');
        urlInput.classList.add('input-invalid');
        return false;
    }
};

const clearURLInput = () => {
    let urlInput = element('urlInput');
    urlInput.value = '';
    urlInput.classList.remove('input-invalid');
    urlInput.classList.remove('input-valid');
}

const handleConversionButtonClick = (evt) => {
    let urlInput = element('urlInput');
    let valid = validateURLOnInput({target: urlInput});
    if(!valid) return;
    let url = getCurrentURL();
    let loc = window.location;
    let path = loc.pathname;
    path = path.startsWith('/') ? path : `/${path}`;
    path = path.endsWith('/') ? path : `${path}/`;
    let newURL = `${loc.protocol}//${loc.hostname}:${loc.port}${path}css${url.split('/css')[1]}`
    if(!CONVERTED_URLS.includes(newURL))
    {
        CONVERTED_URLS.push(newURL);
        clearURLInput();
        displayConvertedURL(url, newURL);
    }
}

const handleDownloadButtonClick = (evt) => {
    let urlInput = element('urlInput');
    let valid = validateURLOnInput({target: urlInput});
    if(!valid) return;
    let url = getCurrentURL();
    let loc = window.location;
    let path = loc.pathname;
    path = path.startsWith('/') ? path : `/${path}`;
    path = path.endsWith('/') ? path : `${path}/`;
    let newURL = `${loc.protocol}//${loc.hostname}:${loc.port}${path}download/css${url.split('/css')[1]}`
    if(!DOWNLOADED_URLS.includes(newURL))
    {
        DOWNLOADED_URLS.push(newURL);
        clearURLInput();
        displayDownloadableURL(url, newURL);
    }
};

const displayConvertedURL = (url, newURL) => {
    let artifacts = element('artifacts');
    let convertedURLDiv = document.createElement('div');
    convertedURLDiv.classList.add('converted-url');
    convertedURLDiv.innerHTML = `
<div class="converted-url-icon center">
    <i class="material-symbols-outlined">link</i>
</div>
<input class="converted-url-input converted-url-input-old" value="${url}" readonly>
<input class="converted-url-input converted-url-input-new" value="${newURL}" readonly>
    `;
    artifacts.appendChild(convertedURLDiv);
};

const displayDownloadableURL = (url, newURL) => {
    let artifacts = element('artifacts');
    let downloadableURLDiv = document.createElement('div');
    downloadableURLDiv.classList.add('downloadable-url');
    downloadableURLDiv.innerHTML = `
<div class="downloadable-url-icon center">
    <i class="material-symbols-outlined">archive</i>
</div>
<input class="downloadable-url-input downloadable-url-input-old" value="${url}" readonly>
<div class="downloadable-url-download-button-carrier center">
    <a class="downloadable-url-download-button" href="${newURL}">Download</a>
</div>
    `;
    artifacts.appendChild(downloadableURLDiv);
}

const getCurrentURL = () => {
    return element('urlInput').value;
}

const updateCSSVariable = (variable, value) => {
    document.documentElement.style.setProperty(
        variable,
        value
    );
};

const initialize = () => {
    let btnDownload = element('btnDownload');
    let btnConvertURL = element('btnConvertURL');
    let urlInput = element('urlInput');
    btnConvertURL.addEventListener(
        'click',
        handleConversionButtonClick
    );
    btnDownload.addEventListener(
        'click',
        handleDownloadButtonClick
    );
    urlInput.addEventListener(
        'input',
        validateURLOnInput
    );

    for(let colorSetting of [
        ['--highlight', HIGHLIGHT_COLOR],
        ['--invalid', INVALID_COLOR],
        ['--primary', PRIMARY_COLOR],
        ['--secondary', SECONDARY_COLOR],
        ['--text', TEXT_COLOR]
    ])
    {
        if(colorSetting[1] === '') continue;
        updateCSSVariable(
            colorSetting[0],
            colorSetting[1]
        );
    }

};

document.addEventListener(
    'DOMContentLoaded',
    initialize,
    false
);