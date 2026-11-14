const { test, expect } = require('@playwright/test');

test('Swagger UI lädt die lokale Spezifikation und zeigt die API-Endpunkte', async ({ page }) => {
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  // Die Prüfung führt keine Anfrage gegen die produktive API aus.
  await page.route('**/*', route => new URL(route.request().url()).origin === 'http://127.0.0.1:4174'
    ? route.continue() : route.abort());
  await page.goto('/');
  await expect(page.locator('.swagger-ui .info .title')).not.toHaveText('');
  await expect(page.locator('.swagger-ui .opblock').first()).toBeVisible();
  await expect.poll(() => page.evaluate(() => window.ui?.specSelectors.specJson().get('openapi') || ''))
    .toMatch(/^3\./);
  expect(errors).toEqual([]);
});
