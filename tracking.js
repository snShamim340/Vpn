document.addEventListener('DOMContentLoaded', function() {
  // Track ad impressions
  document.querySelectorAll('.veil-ad').forEach(ad => {
    const adId = ad.dataset.adId;
    fetch(`/api/ads/impression?ad_id=${adId}`, {
      method: 'POST',
      credentials: 'include'
    });
  });
});