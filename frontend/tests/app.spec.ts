import { test, expect } from '@playwright/test';

test('has title and loads transactions table', async ({ page }) => {
  await page.goto('/');

  // Check for the main page title
  await expect(page.getByRole('heading', { name: 'FinTech Dashboard' })).toBeVisible();

  // Check for the recent transactions table title
  await expect(page.getByRole('heading', { name: 'Recent Transactions' })).toBeVisible();

  // Check that the table header for "Description" is visible
  await expect(page.getByRole('columnheader', { name: 'Description' })).toBeVisible();
  
  // Check that at least one transaction row is rendered by looking for its description
  // This assumes the seed data is in place
  await expect(page.getByRole('cell', { name: 'Groceries' })).toBeVisible();
});
