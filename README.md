# GFO - Google Fonts On-premise

This software is intended to serve the purpose of embedding fonts from Google Fonts on websites and in applications in a manner that complies with the EU GDPR. It acts as a proxy for Google Fonts by providing the endpoints through which fonts from Google are embedded (https://fonts.googleapis.com/css, https://fonts.googleapis.com/css2) itself.

Let's assume that a user visits your website and you have embedded fonts from Google. The user's browser reads the URLs of the fonts from the website's source code and then visits those URLs to download the CSS files and the font files. Thus, the user then visits Google's servers and there is no way to ensure that the user's data is processed by Google in a way that you want.

If you use GFO, the process looks different. You have then replaced on your website all URLs of Google's API for fonts with the address of your self-provided GFO (~~fonts.googleapis.com~~ -> fonts.yourdomain.com). Now the user's browser will no longer visit Google's servers for loading the fonts, but only your GFO instance. This instance will now download the desired fonts from Google's servers, store them locally, and forward only the contents of the locally stored files to the user's browser. Thus, your users are no longer redirected to external servers, but receive any fonts directly from your infrastructure.

**A demo is available [here](https://fonts.bartscherer.io)**.

**The WordPress plugin is available [here](https://github.com/bartscherer/gfo-wordpress-plugin)**.

## The long-term vision

If the opportunity arises for major IT service providers to make GFO available to the public (without collecting visitors' IP addresses, of course), GFO would become usable without hosting itself. So website owners could then easily specify fonts.bigserviceprovider.de in their <link\> tags instead of fonts.googleapis.com and avoid warnings. I would like to do this myself, but I don't have the infrastructure to do it.

**But there is still a lot to do to make GFO even better, see TODO at the very bottom**.

## Use-Cases

- For example, you are a web agency (e.g. webagency.com) and you provide websites for your clients that use Google Fonts. You can host one (or more) instances of GFO (e.g. fonts.webagency.com) and then change the domain from which the fonts are included in the customer websites (e.g. ~~fonts.googleapis.com~~ -> fonts.webagency.com). This way you have immediately and without much manual effort prevented your customers from receiving warnings because of Google Fonts

- You have your own website and server. You can then simply co-host GFO on the same server (e.g. under the path https://mydomain.com/gfo/) and can then obtain the fonts from there. You then no longer have to change the static assets of your website if you want to use a new font, for example. Also, the basis for warnings for the use of Google fonts is then omitted, since they are obtained from your domain (e.g. https://mydomain.com) instead of from Google's servers.

## Advantages of GFO

- **You don't have to worry about warnings** because of embedded fonts from Google.

- **You don't have to embed the fonts locally in each of your applications**, saving you a lot of time with setup and subsequent updates of the fonts in use.

- **Users may have faster loading times** because GFO can be easily co-hosted on your server, reducing the number of external URLs on your site.

- GFO has a graphical interface that allows you to download **any font (CSS and font files) easily as an archive**. So you just need to enter your embedded links and get ready-made "folders" to embed in your application/website.

- GFO provides a [WordPress plugin](https://github.com/bartscherer/gfo) for you too!

## Disadvantages of GFO

- Unfortunately, the behavior of GFO **currently** is not yet equivalent to the behavior of Google's servers. When a browser visits fonts.googleapis.com, Google's API can determine which format to select for the fonts by providing information about the browser itself, which the browser automatically sends along. For example, with the current Firefox, I get the fonts in WOFF2 format. However, since GFO is a proxy, Google responds to each request with the fonts in TrueType format. This is somewhat older and contains, among other things, data that is not relevant for a font that is used on web pages. **The amount of data is therefore higher**. However, should this project find favor, I will be happy to make appropriate adjustments so that WOFF2 is used whenever possible. **Please keep in mind, that even though TTF is older, it will perfectly serve its purpose and shouldn't cause any problems rendering the font for [more than 98% of all users](https://caniuse.com/?search=ttf). I'd assume that the amount of people using Opera Mini as their browser is pretty small.

- The burden for downloading the fonts will be borne by your infrastructure. In a "perfect" world, I would have simply bought my own domain and run GFO there as a service to everyone. However, this is not easily possible because the more users visit your site, the more downloads of the fonts will take place, thus putting more load on your servers. **This is usually not a problem, however, since you can run multiple instances of GFO yourself and each instance can also handle large amounts of requests (about 1000 requests per second in tests)**.

- This software is still under development and has passed tests well in some areas, however I am sure there are use cases that have not been tested yet. **So there is no guarantee that GFO will always work.**

- You will have to host GFO yourself if no one else will do it for you.

## Installation

### Deployment via HTTP

Installing GFO is dead simple. You need any machine with a working Docker installation. The Docker images of GFO can be found [here](https://hub.docker.com/repository/docker/bartscherer/gfo).

In any directory, create the file "gfo.yaml". We will assume the path `/etc/gfo/gfo.yaml` for this example. This file is the configuration file that can be used to pass parameters to GFO.

> Important: The settings are probably mostly irrelevant for you as a user, but you have to pay attention to the following settings: **customization:imprint_url** and **customization:privacy_url**. These two settings should point to your imprint and privacy policy, so that GFO does not create the problem it is supposed to solve (warning letters).

After you have created the file, it could look like this: 

```yaml
customization:
    imprint_url: https://example.com/imprint
    privacy_url: https://example.com/privacy
misc:
    timezone: Europe/Berlin
```

Now you can start GFO with the following command:

`docker run --publish 80:80 --mount type=bind,source=/etc/gfo/gfo.yaml,target=/app/gfo.yaml bartscherer/gfo:latest`

> Of course, you can also use a port other than 80. To do this, change the `--publish 80:80` parameter to `--publish 1234:80`, for example, to make GFO available externally on port 1234.

If you want to always run GFO when starting the operating system (the Docker daemon), please read [this article](https://docs.docker.com/config/containers/start-containers-automatically/).

### Deployment via HTTPS

If you want to deploy GFO via HTTPS, then you should work with a reverse proxy (e.g. nginx, HAProxy). You can find an example e.g. [here](https://leangaurav.medium.com/simplest-https-setup-nginx-reverse-proxy-letsencrypt-ssl-certificate-aws-cloud-docker-4b74569b3c61).

In this case, please also note that you should block HTTP traffic directly to the GFO container if the server is externally reachable (e.g. `--publish 127.0.0.1:80:80` or via firewall).

## TODO

- Find ways to forward the user agent header of the user to Google's API. This would allow to download fonts that do not use TrueType format only.

- Limit the possible requests to specific fonts (so that the service can't be used arbitrarily).

- doc, doc, doc....

- Fix code smells (the project was created on very short notice in two days)

- Integration into e.g. Wordpress to make it even easier to use GFO

- Better UI

- Find some way around the IPC headache to determine which worker is the one that should run the service manager
