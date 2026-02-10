// AlphaX Document Reader – minimal desk helper
frappe.provide("alphax_document_reader");

alphax_document_reader.open_reader = function() {
  frappe.set_route("Page", "document-reader");
};
