class AdRotator {
  constructor() {
    this.ads = [
      '/static/ads/banner_1.html',
      '/static/ads/banner_2.html'
    ];
    this.currentAd = 0;
    this.adInterval = 30000; // 30 seconds
  }

  startRotation(containerId) {
    this.container = document.getElementById(containerId);
    this.rotateAd();
    setInterval(() => this.rotateAd(), this.adInterval);
  }

  async rotateAd() {
    const response = await fetch(this.ads[this.currentAd]);
    const adHtml = await response.text();
    this.container.innerHTML = adHtml;
    this.currentAd = (this.currentAd + 1) % this.ads.length;
  }
}

// Initialize for free users
if (document.body.classList.contains('free-user')) {
  const rotator = new AdRotator();
  rotator.startRotation('ad-container');
}