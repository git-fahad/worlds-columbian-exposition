"""
Base controller class to eliminate code duplication in routes
Following DRY principles
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash

class BaseController:
    """Base controller class with common route handling methods"""
    
    @staticmethod
    def handle_form_submission(service_method, form_data, success_message, error_redirect=None, success_redirect='main.index'):
        """Generic method to handle form submissions"""
        try:
            service_method(form_data)
            flash(success_message, 'success')
            return redirect(url_for(success_redirect))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            if error_redirect:
                return redirect(url_for(error_redirect))
            return None
    
    @staticmethod
    def render_page(template_name, **kwargs):
        """Generic method to render templates"""
        return render_template(template_name, **kwargs)
    
    @staticmethod
    def handle_get_post_route(template_name, service_method=None, success_message=None, success_redirect='main.index'):
        """Generic method to handle GET/POST routes"""
        if request.method == 'POST' and service_method and success_message:
            result = BaseController.handle_form_submission(
                service_method, 
                request.form, 
                success_message, 
                success_redirect=success_redirect
            )
            if result:
                return result
        
        return BaseController.render_page(template_name)
