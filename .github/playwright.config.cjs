const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  workers: 1,
  retries: 0,
  use: { baseURL: 'http://127.0.0.1:4174', trace: 'retain-on-failure' },
  webServer: {
    command: 'python3 -m http.server 4174 --bind 127.0.0.1 --directory ..',
    url: 'http://127.0.0.1:4174',
  },
});
