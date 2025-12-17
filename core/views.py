from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils import *
from .ai_detector import AIContentDetector
import uuid

ai_detector = AIContentDetector()

processing_results = {}

def home(request):
    return render(request, 'core/home.html')

def plagiarism_check(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('document')
        typed_text = request.POST.get('text_input')
        extracted_text = ""
        
        if uploaded_file:
            file_name = uploaded_file.name.lower()
            if file_name.endswith('.txt'):
                extracted_text = extract_text_from_txt(uploaded_file)
            elif file_name.endswith('.docx'):
                extracted_text = extract_text_from_docx(uploaded_file)
            elif file_name.endswith('.pdf'):
                extracted_text = extract_text_from_pdf(uploaded_file)
            else:
                return render(request, 'core/home.html', {'error': 'Unsupported file format.'})
        
        if typed_text and typed_text.strip() != "":
            extracted_text = typed_text
        
        if not extracted_text or extracted_text.strip() == "":
            return render(request, 'core/home.html', {'error': 'No text to analyze.'})
        
        check_id = str(uuid.uuid4())
        
        processing_results[check_id] = {
            'status': 'processing',
            'text': extracted_text
        }
        
        return redirect('loading', check_id=check_id)
    
    return render(request, 'core/home.html')

def loading(request, check_id):
    return render(request, 'core/loading.html', {'check_id': check_id})

def process_check(request, check_id):
    if check_id not in processing_results:
        return JsonResponse({'status': 'error', 'message': 'Invalid check ID'})
    
    result_data = processing_results[check_id]
    
    if result_data['status'] == 'processing':
        extracted_text = result_data['text']
        ai_result = ai_detector.detect(extracted_text)
        
        processing_results[check_id] = {
            'status': 'complete',
            'extracted_text': extracted_text,
            'ai_detection_success': ai_result['success'],
            'ai_prediction': ai_result.get('prediction'),
            'ai_confidence': ai_result.get('confidence'),
            'ai_percentage': ai_result.get("probabilities")['Human-Written'],
            'probabilities': ai_result.get('probabilities'),
        }
    
    return JsonResponse({'status': processing_results[check_id]['status']})

def results(request, check_id):
    if check_id not in processing_results:
        return redirect('home')
    
    result_data = processing_results[check_id]
    if result_data['status'] != 'complete':
        return redirect('loading', check_id=check_id)
    human_percentage = 100 - result_data["probabilities"]['AI-Generated']
    context = {
        'extracted_text': result_data['extracted_text'],
        'ai_detection_success': result_data['ai_detection_success'],
        'ai_prediction': result_data['ai_prediction'],
        'ai_confidence': result_data['ai_confidence'],
        'ai_percentage': result_data['probabilities']['AI-Generated'],
        'probabilities': result_data['probabilities'],
        'human_percentage': human_percentage,
    }
    
    del processing_results[check_id]
    
    return render(request, 'core/analytics.html', context)