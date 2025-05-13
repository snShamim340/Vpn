class SessionTimer {
  constructor(duration, warningCallback, expireCallback) {
    this.duration = duration;
    this.remaining = duration;
    this.warningCallback = warningCallback;
    this.expireCallback = expireCallback;
    this.interval = null;
  }

  start() {
    this.interval = setInterval(() => {
      this.remaining -= 1;
      document.getElementById('session-timer').textContent = 
        this.formatTime(this.remaining);

      if (this.remaining <= 300) { // 5 minute warning
        this.warningCallback(this.remaining);
      }

      if (this.remaining <= 0) {
        this.stop();
        this.expireCallback();
      }
    }, 1000);
  }

  stop() {
    clearInterval(this.interval);
  }

  formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }
}

// Initialize if timer element exists
if (document.getElementById('session-timer')) {
  const duration = parseInt(document.getElementById('session-timer').dataset.duration);
  const timer = new SessionTimer(
    duration,
    (remaining) => {
      // Show warning when 5 minutes remain
      alert(`Your free session will end in ${Math.floor(remaining/60)} minutes`);
    },
    () => {
      // Session expired
      window.location.href = '/session-ended';
    }
  );
  timer.start();
}