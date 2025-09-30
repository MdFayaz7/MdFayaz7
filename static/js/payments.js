// Payment handling JavaScript
class PaymentHandler {
    constructor(razorpayKeyId) {
        this.razorpayKeyId = razorpayKeyId;
        this.isProcessing = false;
    }

    async createOrder(feeType) {
        if (this.isProcessing) return;
        
        this.isProcessing = true;
        this.showLoader();

        try {
            const response = await fetch('/payments/create-order/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ fee_type: feeType })
            });

            const data = await response.json();
            
            if (response.ok) {
                this.initiateRazorpayPayment(data, feeType);
            } else {
                throw new Error(data.error || 'Failed to create order');
            }
        } catch (error) {
            this.showError('Failed to initiate payment: ' + error.message);
        } finally {
            this.hideLoader();
            this.isProcessing = false;
        }
    }

    initiateRazorpayPayment(orderData, feeType) {
        const options = {
            key: this.razorpayKeyId,
            amount: orderData.amount,
            currency: orderData.currency,
            name: 'College Fee Payment',
            description: `Payment for ${feeType.replace('_', ' ').toUpperCase()}`,
            order_id: orderData.order_id,
            handler: (response) => {
                this.verifyPayment(response, orderData.payment_id);
            },
            prefill: {
                name: document.querySelector('[data-student-name]')?.dataset.studentName || '',
                email: document.querySelector('[data-student-email]')?.dataset.studentEmail || '',
                contact: document.querySelector('[data-student-phone]')?.dataset.studentPhone || ''
            },
            theme: {
                color: '#0d6efd'
            },
            modal: {
                ondismiss: () => {
                    this.showError('Payment cancelled by user');
                }
            }
        };

        const rzp = new Razorpay(options);
        rzp.open();
    }

    async verifyPayment(razorpayResponse, paymentId) {
        this.showLoader();

        try {
            const response = await fetch('/payments/verify-payment/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    razorpay_order_id: razorpayResponse.razorpay_order_id,
                    razorpay_payment_id: razorpayResponse.razorpay_payment_id,
                    razorpay_signature: razorpayResponse.razorpay_signature
                })
            });

            const data = await response.json();
            
            if (response.ok && data.success) {
                this.showSuccess('Payment successful!');
                setTimeout(() => {
                    window.location.href = `/payments/payment-success/${data.payment_id}/`;
                }, 2000);
            } else {
                throw new Error(data.error || 'Payment verification failed');
            }
        } catch (error) {
            this.showError('Payment verification failed: ' + error.message);
        } finally {
            this.hideLoader();
        }
    }

    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    showLoader() {
        const loader = document.createElement('div');
        loader.id = 'payment-loader';
        loader.className = 'spinner-overlay';
        loader.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <div class="mt-3 text-white">Processing payment...</div>
            </div>
        `;
        document.body.appendChild(loader);
    }

    hideLoader() {
        const loader = document.getElementById('payment-loader');
        if (loader) {
            loader.remove();
        }
    }

    showSuccess(message) {
        this.showAlert(message, 'success');
    }

    showError(message) {
        this.showAlert(message, 'danger');
    }

    showAlert(message, type) {
        const alertContainer = document.querySelector('.container');
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.innerHTML = `
            <i class="bi bi-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        alertContainer.insertBefore(alert, alertContainer.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }
}

// Initialize payment handler when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const razorpayKeyId = document.querySelector('[data-razorpay-key]')?.dataset.razorpayKey;
    
    if (razorpayKeyId) {
        const paymentHandler = new PaymentHandler(razorpayKeyId);
        
        // Attach event listeners to payment buttons
        document.querySelectorAll('[data-fee-type]').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const feeType = this.dataset.feeType;
                paymentHandler.createOrder(feeType);
            });
        });
    }
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function downloadReceipt(paymentId) {
    window.open(`/payments/download-receipt/${paymentId}/`, '_blank');
}