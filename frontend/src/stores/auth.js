import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        voucherCode: localStorage.getItem('voucherCode') || null,
        voucherData: null,
    }),
    actions: {
        setVoucher(code, data) {
            this.voucherCode = code;
            this.voucherData = data;
            localStorage.setItem('voucherCode', code);
        },
        clearVoucher() {
            this.voucherCode = null;
            this.voucherData = null;
            localStorage.removeItem('voucherCode');
        },
    },
});
