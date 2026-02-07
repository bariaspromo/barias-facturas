/**
 * Simple test suite for Invoice Management System
 */

const { Invoice, InvoiceManager } = require('../src/invoice');

function assert(condition, message) {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
}

function testInvoiceCreation() {
  console.log('Testing invoice creation...');
  const invoice = new Invoice({
    businessType: 'restaurant',
    businessName: 'Test Restaurant',
    customerName: 'Test Customer'
  });
  
  assert(invoice.id !== undefined, 'Invoice should have an ID');
  assert(invoice.businessType === 'restaurant', 'Business type should be restaurant');
  assert(invoice.status === 'pending', 'Initial status should be pending');
  assert(invoice.items.length === 0, 'New invoice should have no items');
  console.log('✓ Invoice creation test passed');
}

function testAddingItems() {
  console.log('Testing adding items...');
  const invoice = new Invoice({
    businessType: 'restaurant',
    businessName: 'Test Restaurant'
  });
  
  invoice.addItem({
    name: 'Test Item',
    price: 10.00,
    quantity: 2
  });
  
  assert(invoice.items.length === 1, 'Invoice should have 1 item');
  assert(invoice.subtotal === 20.00, 'Subtotal should be 20.00');
  assert(invoice.tax > 0, 'Tax should be calculated');
  assert(invoice.total > invoice.subtotal, 'Total should include tax');
  console.log('✓ Adding items test passed');
}

function testTaxCalculation() {
  console.log('Testing tax calculation...');
  
  // Test restaurant tax (10%)
  const restaurantInvoice = new Invoice({
    businessType: 'restaurant',
    businessName: 'Test Restaurant'
  });
  restaurantInvoice.addItem({ name: 'Item', price: 100, quantity: 1 });
  assert(restaurantInvoice.tax === 10.00, 'Restaurant tax should be 10%');
  
  // Test bar tax (15%)
  const barInvoice = new Invoice({
    businessType: 'bar',
    businessName: 'Test Bar'
  });
  barInvoice.addItem({ name: 'Item', price: 100, quantity: 1 });
  assert(barInvoice.tax === 15.00, 'Bar tax should be 15%');
  
  // Test liquor store tax (18%)
  const liquorInvoice = new Invoice({
    businessType: 'liquor-store',
    businessName: 'Test Liquor Store'
  });
  liquorInvoice.addItem({ name: 'Item', price: 100, quantity: 1 });
  assert(liquorInvoice.tax === 18.00, 'Liquor store tax should be 18%');
  
  console.log('✓ Tax calculation test passed');
}

function testInvoiceStatus() {
  console.log('Testing invoice status changes...');
  const invoice = new Invoice({
    businessType: 'restaurant',
    businessName: 'Test Restaurant'
  });
  
  assert(invoice.status === 'pending', 'Initial status should be pending');
  
  invoice.markAsPaid();
  assert(invoice.status === 'paid', 'Status should be paid after marking as paid');
  
  const invoice2 = new Invoice({
    businessType: 'bar',
    businessName: 'Test Bar'
  });
  invoice2.cancel();
  assert(invoice2.status === 'cancelled', 'Status should be cancelled after cancelling');
  
  console.log('✓ Invoice status test passed');
}

function testInvoiceManager() {
  console.log('Testing invoice manager...');
  const manager = new InvoiceManager();
  
  const invoice1 = manager.createInvoice({
    businessType: 'restaurant',
    businessName: 'Restaurant 1'
  });
  
  const invoice2 = manager.createInvoice({
    businessType: 'bar',
    businessName: 'Bar 1'
  });
  
  assert(manager.getAllInvoices().length === 2, 'Manager should have 2 invoices');
  
  const foundInvoice = manager.getInvoice(invoice1.id);
  assert(foundInvoice !== undefined, 'Should find invoice by ID');
  assert(foundInvoice.id === invoice1.id, 'Found invoice should match');
  
  const restaurants = manager.getInvoicesByBusinessType('restaurant');
  assert(restaurants.length === 1, 'Should have 1 restaurant invoice');
  
  console.log('✓ Invoice manager test passed');
}

function testRevenueCalculation() {
  console.log('Testing revenue calculation...');
  const manager = new InvoiceManager();
  
  const invoice1 = manager.createInvoice({
    businessType: 'restaurant',
    businessName: 'Restaurant 1'
  });
  invoice1.addItem({ name: 'Item', price: 100, quantity: 1 });
  invoice1.markAsPaid();
  
  const invoice2 = manager.createInvoice({
    businessType: 'bar',
    businessName: 'Bar 1'
  });
  invoice2.addItem({ name: 'Item', price: 50, quantity: 1 });
  invoice2.markAsPaid();
  
  const invoice3 = manager.createInvoice({
    businessType: 'restaurant',
    businessName: 'Restaurant 2'
  });
  invoice3.addItem({ name: 'Item', price: 75, quantity: 1 });
  // Not marking as paid - should not count in revenue
  
  const restaurantRevenue = manager.getTotalRevenue('restaurant');
  assert(restaurantRevenue === 110.00, 'Restaurant revenue should be 110.00 (100 + 10% tax)');
  
  const totalRevenue = manager.getTotalRevenue();
  assert(totalRevenue > 0, 'Total revenue should be positive');
  
  console.log('✓ Revenue calculation test passed');
}

function testRemoveItem() {
  console.log('Testing item removal...');
  const invoice = new Invoice({
    businessType: 'restaurant',
    businessName: 'Test Restaurant'
  });
  
  invoice.addItem({ name: 'Item 1', price: 10, quantity: 1 });
  invoice.addItem({ name: 'Item 2', price: 20, quantity: 1 });
  invoice.addItem({ name: 'Item 3', price: 30, quantity: 1 });
  
  assert(invoice.items.length === 3, 'Should have 3 items');
  const initialTotal = invoice.total;
  
  invoice.removeItem(1); // Remove middle item
  assert(invoice.items.length === 2, 'Should have 2 items after removal');
  assert(invoice.total < initialTotal, 'Total should decrease after removal');
  
  console.log('✓ Item removal test passed');
}

function runTests() {
  console.log('\n=== Running Invoice Management System Tests ===\n');
  
  try {
    testInvoiceCreation();
    testAddingItems();
    testTaxCalculation();
    testInvoiceStatus();
    testInvoiceManager();
    testRevenueCalculation();
    testRemoveItem();
    
    console.log('\n✓ All tests passed!\n');
    process.exit(0);
  } catch (error) {
    console.error(`\n✗ Test failed: ${error.message}\n`);
    console.error(error.stack);
    process.exit(1);
  }
}

runTests();
