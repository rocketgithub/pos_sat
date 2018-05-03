odoo.define('pos_sat.pos_sat', function (require) {
"use strict";

var models = require('point_of_sale.models');
var screens = require('point_of_sale.screens');

var _super_posmodel = models.PosModel.prototype;
models.PosModel = models.PosModel.extend({
    load_orders: function() {
        var result = _super_posmodel.load_orders.apply(this, arguments);

        this.config.ultimo_numero_factura = 0;
        if (parseInt(this.sale_journal.ultimo_numero_factura)) {
            this.config.ultimo_numero_factura = parseInt(this.sale_journal.ultimo_numero_factura);
        }

        return result;
    },

    add_new_order: function(){
        var posmodel = this;
        if (this.sale_journal.requiere_resolucion && !this.sale_journal.resolucion_id) {
            this.gui.show_popup("error",{
                "title": "Resolución",
                "body":  "No puede abrir la sesión por que no tiene una resolución ingresada.",
            });
            return;
        } else if (this.sale_journal.requiere_resolucion && this.sale_journal.resolucion_id) {
            var total_documentos = this.sale_journal.final_resolucion - this.sale_journal.inicial_resolucion + 1;
            var restantes = this.sale_journal.final_resolucion - this.config.ultimo_numero_factura;
            if (this.config.ultimo_numero_factura >= this.sale_journal.final_resolucion) {
                this.gui.show_popup("error",{
                    "title": "Número de factura",
                    "body":  "Ya no existen números de factura para esta serie, por lo cual ya no puede realizar ventas. Por favor pida que le habiliten una nueva serie.",
                });
                return;
            } else if (restantes / total_documentos <= 0.25) {
                this.gui.show_popup("confirm",{
                    "title": "Número de factura",
                    "body":  "Ya solo queda el 25% de números de facturas para esta serie. Por favor avise para que le habiliten una nueva serie pronto.",
                    "confirm": function() {
                        var result = _super_posmodel.add_new_order.apply(posmodel);
                        return result;
                    },
                });
            } else {
                var result = _super_posmodel.add_new_order.apply(posmodel);
                return result;
            }
        } else {
            var result = _super_posmodel.add_new_order.apply(posmodel);
            return result;
        }
    },

    push_and_invoice_order: function(order){
        if (this.sale_journal.requiere_resolucion && !('numero_factura_impreso' in order)) {
            this.config.ultimo_numero_factura += 1;
            order.numero_factura_impreso = this.config.ultimo_numero_factura;
        }
        var result = _super_posmodel.push_and_invoice_order.apply(this, arguments);
        return result;
    },
})

var _super_order = models.Order.prototype;
models.Order = models.Order.extend({
    export_as_JSON: function(){
        var json = _super_order.export_as_JSON.apply(this);
        if (this.pos.sale_journal.requiere_resolucion) {
            json['numero_factura_impreso'] = this.numero_factura_impreso;
        }
        return json;
    }
})

// var _super_receipt = screens.ReceiptScreenWidget.prototype;
// screens.ReceiptScreenWidget.include({
//     handle_auto_print: function(){
//         this.print_web();
//     }
// })

});
