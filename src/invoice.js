/**
 * Invoice Management System
 * Core module for managing invoices for restaurants, bars, and liquor stores
 */

class Invoice {
  constructor(data) {
    this.id = data.id || this.generateId();
    this.businessType = data.businessType; // 'restaurant', 'bar', 'liquor-store'
    this.businessName = data.businessName;
    this.customerName = data.customerName || 'Walk-in Customer';
    this.date = data.date || new Date().toISOString();
    this.items = data.items || [];
    this.subtotal = 0;
    this.tax = 0;
    this.total = 0;
    this.status = data.status || 'pending'; // pending, paid, cancelled
    
    this.calculateTotals();
  }

  generateId() {
    return 'INV-' + Date.now() + '-' + Math.floor(Math.random() * 1000);
  }

  calculateTotals() {
    this.subtotal = this.items.reduce((sum, item) => {
      return sum + (item.price * item.quantity);
    }, 0);
    
    // Different tax rates by business type
    const taxRates = {
      'restaurant': 0.10,  // 10% tax
      'bar': 0.15,         // 15% tax
      'liquor-store': 0.18 // 18% tax
    };
    
    const taxRate = taxRates[this.businessType] || 0.10;
    this.tax = this.subtotal * taxRate;
    this.total = this.subtotal + this.tax;
  }

  addItem(item) {
    if (!item.name || !item.price || !item.quantity) {
      throw new Error('Item must have name, price, and quantity');
    }
    this.items.push(item);
    this.calculateTotals();
  }

  removeItem(index) {
    if (index >= 0 && index < this.items.length) {
      this.items.splice(index, 1);
      this.calculateTotals();
    }
  }

  markAsPaid() {
    this.status = 'paid';
  }

  cancel() {
    this.status = 'cancelled';
  }

  toJSON() {
    return {
      id: this.id,
      businessType: this.businessType,
      businessName: this.businessName,
      customerName: this.customerName,
      date: this.date,
      items: this.items,
      subtotal: this.subtotal.toFixed(2),
      tax: this.tax.toFixed(2),
      total: this.total.toFixed(2),
      status: this.status
    };
  }

  toString() {
    let output = '\n=== INVOICE ===\n';
    output += `ID: ${this.id}\n`;
    output += `Business: ${this.businessName} (${this.businessType})\n`;
    output += `Customer: ${this.customerName}\n`;
    output += `Date: ${new Date(this.date).toLocaleDateString()}\n`;
    output += `Status: ${this.status.toUpperCase()}\n`;
    output += '\nITEMS:\n';
    output += '--------------------------------------------\n';
    
    this.items.forEach((item, index) => {
      output += `${index + 1}. ${item.name} x${item.quantity} @ $${item.price.toFixed(2)} = $${(item.price * item.quantity).toFixed(2)}\n`;
    });
    
    output += '--------------------------------------------\n';
    output += `Subtotal: $${this.subtotal.toFixed(2)}\n`;
    output += `Tax: $${this.tax.toFixed(2)}\n`;
    output += `TOTAL: $${this.total.toFixed(2)}\n`;
    output += '============================================\n';
    
    return output;
  }
}

class InvoiceManager {
  constructor() {
    this.invoices = [];
  }

  createInvoice(data) {
    const invoice = new Invoice(data);
    this.invoices.push(invoice);
    return invoice;
  }

  getInvoice(id) {
    return this.invoices.find(inv => inv.id === id);
  }

  getAllInvoices() {
    return this.invoices;
  }

  getInvoicesByBusinessType(businessType) {
    return this.invoices.filter(inv => inv.businessType === businessType);
  }

  getInvoicesByStatus(status) {
    return this.invoices.filter(inv => inv.status === status);
  }

  getTotalRevenue(businessType = null) {
    let invoices = this.invoices.filter(inv => inv.status === 'paid');
    
    if (businessType) {
      invoices = invoices.filter(inv => inv.businessType === businessType);
    }
    
    return invoices.reduce((sum, inv) => sum + inv.total, 0);
  }

  deleteInvoice(id) {
    const index = this.invoices.findIndex(inv => inv.id === id);
    if (index !== -1) {
      this.invoices.splice(index, 1);
      return true;
    }
    return false;
  }
}

module.exports = { Invoice, InvoiceManager };
