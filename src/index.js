#!/usr/bin/env node

/**
 * Barias Facturas - Invoice Management System
 * Main entry point demonstrating the invoice system
 */

const { Invoice, InvoiceManager } = require('./invoice');

function main() {
  console.log('=== Barias Facturas - Invoice Management System ===\n');
  
  // Create invoice manager
  const manager = new InvoiceManager();
  
  // Example 1: Create a restaurant invoice
  console.log('Creating restaurant invoice...');
  const restaurantInvoice = manager.createInvoice({
    businessType: 'restaurant',
    businessName: 'La Casa de Barias',
    customerName: 'John Doe'
  });
  
  restaurantInvoice.addItem({
    name: 'Grilled Steak',
    price: 25.99,
    quantity: 2
  });
  
  restaurantInvoice.addItem({
    name: 'Caesar Salad',
    price: 8.50,
    quantity: 2
  });
  
  restaurantInvoice.addItem({
    name: 'Soft Drink',
    price: 3.00,
    quantity: 2
  });
  
  console.log(restaurantInvoice.toString());
  restaurantInvoice.markAsPaid();
  
  // Example 2: Create a bar invoice
  console.log('\nCreating bar invoice...');
  const barInvoice = manager.createInvoice({
    businessType: 'bar',
    businessName: 'Barias Sports Bar',
    customerName: 'Jane Smith'
  });
  
  barInvoice.addItem({
    name: 'Craft Beer',
    price: 7.50,
    quantity: 4
  });
  
  barInvoice.addItem({
    name: 'Nachos',
    price: 12.00,
    quantity: 1
  });
  
  barInvoice.addItem({
    name: 'Wings',
    price: 15.00,
    quantity: 1
  });
  
  console.log(barInvoice.toString());
  barInvoice.markAsPaid();
  
  // Example 3: Create a liquor store invoice
  console.log('\nCreating liquor store invoice...');
  const liquorInvoice = manager.createInvoice({
    businessType: 'liquor-store',
    businessName: 'Barias Liquor Emporium'
  });
  
  liquorInvoice.addItem({
    name: 'Premium Whiskey',
    price: 45.00,
    quantity: 2
  });
  
  liquorInvoice.addItem({
    name: 'Red Wine',
    price: 22.00,
    quantity: 3
  });
  
  console.log(liquorInvoice.toString());
  liquorInvoice.markAsPaid();
  
  // Display summary
  console.log('\n=== BUSINESS SUMMARY ===\n');
  console.log(`Total Invoices: ${manager.getAllInvoices().length}`);
  console.log(`Paid Invoices: ${manager.getInvoicesByStatus('paid').length}`);
  console.log(`Pending Invoices: ${manager.getInvoicesByStatus('pending').length}`);
  console.log('\nRevenue by Business Type:');
  console.log(`  Restaurant: $${manager.getTotalRevenue('restaurant').toFixed(2)}`);
  console.log(`  Bar: $${manager.getTotalRevenue('bar').toFixed(2)}`);
  console.log(`  Liquor Store: $${manager.getTotalRevenue('liquor-store').toFixed(2)}`);
  console.log(`\nTotal Revenue: $${manager.getTotalRevenue().toFixed(2)}`);
  console.log('\n==============================================\n');
}

// Run the demo
if (require.main === module) {
  main();
}

module.exports = { main };
