from django import  forms
from tasks.models import Tasks,TaskDetail

# Django From
class TaskForm(forms.Form):
    title=forms.CharField(max_length=250,label="Task Title")
    description= forms.CharField(widget=forms.Textarea,label="Task Description")
    due_date=forms.DateField(widget=forms.SelectDateWidget,label="Due Date")
    assigned_to=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[],label="Assigned To")
    
    def __init__(self, *args, **kwargs):
        employees=kwargs.pop('employees',[])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices=[(emp.id,emp.name)for emp in employees]

class StyleFromMixin:
    '''Mixin to apply styles to from fields'''
    default_classes= "border-2 border-gray-400 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500 focus:outline-none"
    
    def apply_style_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none rounded-md",
                    'placeholder': f"Enter {field.label.lower()}",
                
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': "border-2 border-gray-400  rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500 focus:outline-none"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':"space-y-2"
                })
            elif isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter The password"
                })
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })
    def __init__(self,*arg,**kwargs):
        super().__init__(*arg,**kwargs)
        self.apply_style_widgets() 
        
#  Django Models from
class TasksModelForm(StyleFromMixin,forms.ModelForm):
    class Meta:
        model=Tasks
        fields=['title','description','due_date','assigned_to']
        widgets={
            'due_date':forms.SelectDateWidget,
            'assigned_to':forms.CheckboxSelectMultiple
        }
        
        # exclude=['project','is_complete','created_at','updated_at']
        # it is is use for when we need value dont want to use it
        '''Manual Widget'''
        # widgets={
        #     'title': forms.TextInput(attrs={
        #         'class':"border-2 border-gray-400 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500 focus:outline-none ",
        #         'placeholder':"Enter Your Task Title"
                
        #         }),
        #     'description': forms.Textarea(attrs={
        #         'class':"border-2 border-gray-400 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500 focus:outline-none ",
        #         'placeholder':"Enter The Description of Task"
        #         }),
        #     'due_date':forms.SelectDateWidget(
        #         attrs={
        #             'class':"border-2 border-gray-400 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500 focus:outline-none"
        #         }
        #         ),
        #     'assigned_to':forms.CheckboxSelectMultiple(attrs={
        #         'class':"border-2 border-gray-400 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500 focus:outline-none w-4 h-4 text-blue-800 focus:ring-red-500 focus:ring-2"
        #         }),
        # }
    ''' widget using Mixins'''
    def __init__(self,*arg,**kwargs):
        super().__init__(*arg,**kwargs)
        self.apply_style_widgets()
        
class TaskDetailModelFrom(StyleFromMixin,forms.ModelForm):
       class Meta:
           model = TaskDetail
           fields=['priority', 'notes']
        
       def __init__(self,*arg,**kwargs):
          super().__init__(*arg,**kwargs)
          self.apply_style_widgets() 
           
