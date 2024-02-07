class BtnTitleMixin:
    btn_title = None
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['btn_title'] = self.btn_title
        return context