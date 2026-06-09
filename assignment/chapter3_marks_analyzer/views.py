from django.shortcuts import render
import pandas as pd
import numpy as np
from pathlib import Path
import os


def get_marks_file():
    """Get or create marks CSV file path"""
    base_dir = Path(__file__).resolve().parent
    marks_file = base_dir / 'marks_data.csv'
    return marks_file


def index(request):
    """Display marks analyzer menu"""
    return render(request, 'chapter3_marks_analyzer/index.html')


def upload_data(request):
    """Upload marks data"""
    if request.method == 'POST':
        import csv
        data = request.POST.get('data', '').strip()
        marks_file = get_marks_file()
        
        try:
            lines = data.split('\n')
            if len(lines) < 2:
                return render(request, 'chapter3_marks_analyzer/upload_data.html', 
                            {'error': 'Please provide headers and at least one data row'})
            
            with open(marks_file, 'w', newline='') as f:
                f.write(data)
            
            return render(request, 'chapter3_marks_analyzer/upload_data.html', 
                        {'success': 'Data uploaded successfully!'})
        except Exception as e:
            return render(request, 'chapter3_marks_analyzer/upload_data.html', 
                        {'error': f'Error: {str(e)}'})
    
    return render(request, 'chapter3_marks_analyzer/upload_data.html')


def view_data(request):
    """View raw data"""
    marks_file = get_marks_file()
    
    try:
        df = pd.read_csv(marks_file)
        data_html = df.to_html(classes='table')
        return render(request, 'chapter3_marks_analyzer/view_data.html', {'data_html': data_html})
    except Exception as e:
        return render(request, 'chapter3_marks_analyzer/view_data.html', 
                    {'error': f'Error reading data: {str(e)}'})


def statistics(request):
    """Display statistics"""
    marks_file = get_marks_file()
    stats = {}
    
    try:
        df = pd.read_csv(marks_file)
        
        # Find numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            stats[col] = {
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                'count': df[col].count()
            }
        
        return render(request, 'chapter3_marks_analyzer/statistics.html', {'stats': stats})
    except Exception as e:
        return render(request, 'chapter3_marks_analyzer/statistics.html', 
                    {'error': f'Error: {str(e)}'})


def grouping(request):
    """Group and analyze data"""
    marks_file = get_marks_file()
    result = {}
    error = None
    
    if request.method == 'POST':
        group_col = request.POST.get('group_column', '')
        try:
            df = pd.read_csv(marks_file)
            if group_col not in df.columns:
                error = f"Column '{group_col}' not found"
            else:
                grouped = df.groupby(group_col).size()
                result = grouped.to_dict()
        except Exception as e:
            error = str(e)
    
    try:
        df = pd.read_csv(marks_file)
        columns = list(df.columns)
    except:
        columns = []
    
    return render(request, 'chapter3_marks_analyzer/grouping.html', 
                {'result': result, 'columns': columns, 'error': error})


def filtering(request):
    """Filter data"""
    marks_file = get_marks_file()
    filtered_data = None
    error = None
    columns = []
    
    if request.method == 'POST':
        try:
            df = pd.read_csv(marks_file)
            columns = list(df.columns)
            
            column = request.POST.get('column')
            operator = request.POST.get('operator')
            value = request.POST.get('value')
            
            if column not in df.columns:
                error = f"Column '{column}' not found"
            else:
                try:
                    # Try to convert to numeric
                    numeric_value = float(value)
                except:
                    numeric_value = value
                
                if operator == 'equals':
                    filtered_df = df[df[column] == numeric_value]
                elif operator == 'greater':
                    filtered_df = df[df[column] > numeric_value]
                elif operator == 'less':
                    filtered_df = df[df[column] < numeric_value]
                elif operator == 'contains':
                    filtered_df = df[df[column].astype(str).str.contains(str(value))]
                
                filtered_data = filtered_df.to_html(classes='table') if not filtered_df.empty else '<p>No matching records</p>'
        except Exception as e:
            error = str(e)
    else:
        try:
            df = pd.read_csv(marks_file)
            columns = list(df.columns)
        except:
            columns = []
    
    return render(request, 'chapter3_marks_analyzer/filtering.html', 
                {'filtered_data': filtered_data, 'columns': columns, 'error': error})


def sorting(request):
    """Sort data"""
    marks_file = get_marks_file()
    sorted_data = None
    error = None
    columns = []
    
    if request.method == 'POST':
        try:
            df = pd.read_csv(marks_file)
            columns = list(df.columns)
            
            sort_col = request.POST.get('sort_column')
            order = request.POST.get('order') == 'descending'
            
            if sort_col not in df.columns:
                error = f"Column '{sort_col}' not found"
            else:
                sorted_df = df.sort_values(by=sort_col, ascending=not order)
                sorted_data = sorted_df.to_html(classes='table')
        except Exception as e:
            error = str(e)
    else:
        try:
            df = pd.read_csv(marks_file)
            columns = list(df.columns)
        except:
            columns = []
    
    return render(request, 'chapter3_marks_analyzer/sorting.html', 
                {'sorted_data': sorted_data, 'columns': columns, 'error': error})
