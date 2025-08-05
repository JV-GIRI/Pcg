import os
from supabase import create_client, Client
from datetime import datetime
import json
from typing import Dict, List, Optional
from config import SUPABASE_URL, SUPABASE_KEY

class SupabaseManager:
    def __init__(self):
        if SUPABASE_URL and SUPABASE_KEY:
            self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        else:
            self.supabase = None
            print("Warning: Supabase credentials not found. Using local storage.")
    
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        if not self.supabase:
            return False
            
        try:
            # Patients table
            self.supabase.table('patients').select('*').limit(1).execute()
        except Exception:
            # Table doesn't exist, create it
            print("Creating patients table...")
            
        try:
            # Cases table  
            self.supabase.table('cases').select('*').limit(1).execute()
        except Exception:
            print("Creating cases table...")
            
        return True
    
    def save_patient(self, patient_data: Dict) -> Optional[str]:
        """Save patient information and return patient ID"""
        if not self.supabase:
            return self._save_patient_local(patient_data)
            
        try:
            patient_record = {
                'name': patient_data['name'],
                'age': patient_data['age'],
                'gender': patient_data['gender'],
                'height': patient_data.get('height'),
                'weight': patient_data.get('weight'),
                'bmi': patient_data.get('bmi'),
                'phone': patient_data.get('phone'),
                'clinical_notes': patient_data.get('clinical_notes'),
                'created_at': datetime.now().isoformat()
            }
            
            response = self.supabase.table('patients').insert(patient_record).execute()
            return response.data[0]['id'] if response.data else None
            
        except Exception as e:
            print(f"Error saving patient: {e}")
            return self._save_patient_local(patient_data)
    
    def save_case(self, case_data: Dict) -> bool:
        """Save diagnosis case"""
        if not self.supabase:
            return self._save_case_local(case_data)
            
        try:
            case_record = {
                'patient_id': case_data['patient_id'],
                'valve_site': case_data['valve_site'],
                'audio_filename': case_data['audio_filename'],
                'diagnosis': json.dumps(case_data['diagnosis']),
                'confidence_level': case_data.get('confidence_level'),
                'severity': case_data.get('severity'),
                'recommendations': case_data.get('recommendations'),
                'created_at': datetime.now().isoformat()
            }
            
            response = self.supabase.table('cases').insert(case_record).execute()
            return len(response.data) > 0
            
        except Exception as e:
            print(f"Error saving case: {e}")
            return self._save_case_local(case_data)
    
    def get_patient_cases(self, patient_id: str) -> List[Dict]:
        """Get all cases for a patient"""
        if not self.supabase:
            return self._get_patient_cases_local(patient_id)
            
        try:
            response = self.supabase.table('cases').select('*').eq('patient_id', patient_id).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching patient cases: {e}")
            return []
    
    def get_all_patients(self) -> List[Dict]:
        """Get all patients"""
        if not self.supabase:
            return self._get_all_patients_local()
            
        try:
            response = self.supabase.table('patients').select('*').order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching patients: {e}")
            return []
    
    def get_case_history(self) -> List[Dict]:
        """Get complete case history with patient details"""
        if not self.supabase:
            return self._get_case_history_local()
            
        try:
            response = self.supabase.table('cases').select('''
                *,
                patients (
                    name,
                    age,
                    gender,
                    bmi,
                    clinical_notes
                )
            ''').order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching case history: {e}")
            return []
    
    # Local storage fallback methods
    def _save_patient_local(self, patient_data: Dict) -> str:
        """Fallback local storage for patient data"""
        import uuid
        patient_id = str(uuid.uuid4())
        
        patients_file = "local_patients.json"
        patients = []
        
        if os.path.exists(patients_file):
            with open(patients_file, 'r') as f:
                patients = json.load(f)
        
        patient_data['id'] = patient_id
        patient_data['created_at'] = datetime.now().isoformat()
        patients.append(patient_data)
        
        with open(patients_file, 'w') as f:
            json.dump(patients, f, indent=2)
            
        return patient_id
    
    def _save_case_local(self, case_data: Dict) -> bool:
        """Fallback local storage for case data"""
        cases_file = "local_cases.json"
        cases = []
        
        if os.path.exists(cases_file):
            with open(cases_file, 'r') as f:
                cases = json.load(f)
        
        case_data['created_at'] = datetime.now().isoformat()
        cases.append(case_data)
        
        with open(cases_file, 'w') as f:
            json.dump(cases, f, indent=2)
            
        return True
    
    def _get_all_patients_local(self) -> List[Dict]:
        """Get all patients from local storage"""
        patients_file = "local_patients.json"
        if os.path.exists(patients_file):
            with open(patients_file, 'r') as f:
                return json.load(f)
        return []
    
    def _get_patient_cases_local(self, patient_id: str) -> List[Dict]:
        """Get patient cases from local storage"""
        cases_file = "local_cases.json"
        if os.path.exists(cases_file):
            with open(cases_file, 'r') as f:
                cases = json.load(f)
                return [case for case in cases if case.get('patient_id') == patient_id]
        return []
    
    def _get_case_history_local(self) -> List[Dict]:
        """Get case history from local storage"""
        patients = self._get_all_patients_local()
        cases_file = "local_cases.json"
        
        if os.path.exists(cases_file):
            with open(cases_file, 'r') as f:
                cases = json.load(f)
                
            # Join with patient data
            for case in cases:
                patient = next((p for p in patients if p['id'] == case['patient_id']), None)
                if patient:
                    case['patient'] = patient
                    
            return cases
        return []

# Global database instance
db = SupabaseManager()