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
                // this.gui.show_popup("confirm",{
                //     "title": "Número de factura",
                //     "body":  "Ya solo queda el 25% de números de facturas para esta serie. Por favor avise para que le habiliten una nueva serie pronto.",
                //     "confirm": function() {
                //         var result = _super_posmodel.add_new_order.apply(posmodel);
                //         return result;
                //     },
                // });
                var result = _super_posmodel.add_new_order.apply(posmodel);
                return result;
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
        var json = _super_order.export_as_JSON.apply(this, arguments);
        if (this.pos.sale_journal.requiere_resolucion) {
            json['numero_factura_impreso'] = this.numero_factura_impreso;
        }
        return json;
    }
})

var _super_payment = screens.PaymentScreenWidget.prototype;
screens.PaymentScreenWidget.include({
    validate_order: function(force_validation){
        var order = this.pos.get_order();
        if (this.pos.sale_journal.requiere_resolucion && !('numero_factura_impreso' in order)) {
            this.pos.config.ultimo_numero_factura += 1;
            order.numero_factura_impreso = this.pos.config.ultimo_numero_factura;
        }
        if (this.order_is_valid(force_validation)) {
            this.finalize_validation();
        }
    }
})

//screens.ReceiptScreenWidget.include({
//    print_web: function(){
//        var widget = this;
//        var order = this.pos.get_order();
//        var receipt = order.export_for_printing();
//        var orderlines = order.get_orderlines();
//        var paymentlines = order.get_paymentlines();
//
//        var serie = widget.pos.sale_journal.serie_resolucion;
//        var resolucion = widget.pos.sale_journal.name_resolucion;
//        var del = widget.pos.sale_journal.inicial_resolucion;
//        var al = widget.pos.sale_journal.final_resolucion;
//        var fecha = widget.pos.sale_journal.fecha_resolucion;
//        var direccion = widget.pos.sale_journal.direccion_resolucion;
//
//        var ticket = order.name+"<BR>";
//        ticket += widget.pos.config.name+"<BR>";
//        ticket += widget.pos.company.name+"<BR>";
//        if (receipt.header) {
//            ticket += receipt.header+"<BR>";
//        }
//        ticket += direccion+"<BR>";
//        ticket += "NIT: "+widget.pos.company.vat+"<BR>";
//        ticket += "Serie: "+serie+"<BR>";
//        ticket += "Resolución: "+resolucion+"<BR>";
//        ticket += "Del: "+del+" al: "+al+"<BR>";
//        ticket += "Fecha Resolución: "+moment(fecha).format('L')+"<BR>";
//        ticket += "Vigente hasta: "+moment(widget.pos.sale_journal.fecha_vencimiento_resolucion).format('L')+"<BR>";
//        ticket += "-ORIGINAL-<BR>";
//        ticket += "Factura No.: "+serie+"-"+order.numero_factura_impreso+"<BR><BR>";
//        ticket += "Fecha: "+moment(order.creation_date).format('L LT')+"<BR>";
//        ticket += "Usuario: "+(widget.pos.cashier ? widget.pos.cashier.name : widget.pos.user.name)+"<BR>";
//        if (order.tag_number) {
//            ticket += "Etiqueta: "+order.tag_number+"<BR>";
//        }
//        if (order.take_out) {
//            ticket += "Para llevar<BR>";
//        }
//        if (order.get_client().vat && (order.get_client().vat == 'CF' || order.get_client().vat == 'C/F')) {
//            ticket += "NIT: _________________________<BR>";
//            ticket += "Nombre: ______________________<BR>";
//        } else {
//            ticket += "NIT: "+(order.get_client().vat ? order.get_client().vat : '')+"<BR>";
//            ticket += "Nombre: "+order.get_client().name+"<BR>";
//        }
//        ticket += "Cant    Producto    Precio<BR>";
//        orderlines.forEach(function(orderline) {
//            ticket += orderline.get_quantity_str_with_unit()+"    "+orderline.get_product().display_name+"    "+widget.format_currency(orderline.get_display_price())+"<BR>";
//        })
//        ticket += "Total: "+widget.format_currency(order.get_total_with_tax())+"<BR>";
//        paymentlines.forEach(function(line) {
//            ticket += line.name+": "+widget.format_currency(line.get_amount())+"<BR>";
//        })
//        ticket += "Cambio: "+widget.format_currency(order.get_change())+"<BR>";
//        ticket += "Sujeto a pagos trimestrales<BR>";
//        if (receipt.footer) {
//            ticket += receipt.footer+"<BR>";
//        }
//        ticket += "<BR><BR>-<BR><BR>-<BR><BR><CUT><BR><BR>-<BR><BR><BR>-<BR><BR>-<BR><BR>";
//
//        var comanda = order.name+"<BR>";
//        comanda += widget.pos.config.name+"<BR>";
//        if (order.tag_number) {
//            comanda += "Etiqueta: "+order.tag_number+"<BR>";
//        }
//        if (order.take_out) {
//            comanda += "Para llevar<BR>";
//        }
//        comanda += "Fecha: "+moment(order.creation_date).format('L LT')+"<BR>";
//        comanda += "Usuario: "+(widget.pos.cashier ? widget.pos.cashier.name : widget.pos.user.name)+"<BR>";
//        comanda += "Cant    Producto<BR>";
//        orderlines.forEach(function(orderline) {
//            comanda += orderline.get_quantity_str_with_unit()+"    "+orderline.get_product().display_name+"<BR>";
//        })
//        comanda += "<BR><BR>-<BR><BR>-<BR><BR><CUT><BR><BR>-<BR><BR><BR>-<BR><BR>-<BR><BR>";
//
//        var textoTicket = "";
//        textoTicket += encodeURI(ticket);
//        textoTicket += encodeURI(ticket.replace(/-ORIGINAL-/, '-COPIA-'));
//        textoTicket += encodeURI(comanda);
//        window.location.href="intent://"+textoTicket+"#Intent;scheme=quickprinter;package=pe.diegoveloper.printerserverapp;end;";
//    }
//})

//var _super_receipt = screens.ReceiptScreenWidget.prototype;
//screens.ReceiptScreenWidget.include({
// handle_auto_print: function(){
//     this.print_web();
// }
//})

});
