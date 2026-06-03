import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

def rasp_runtime_monitor(command):
    """الـ RASP الداخلي: يحبط الهجوم ويحمي السيرفر دون إسقاط الخدمة"""
    # مؤشرات مشبوهة (مبسطة لغرض المحاكاة)
    suspicious_indicators = ["cat /etc/passwd", "id", "whoami", "shadow", "wget", "curl"]
    
    # تحويل الأمر للحروف الصغيرة لمنع التلاعب بحالة الأحرف
    normalized_command = command.lower()
    
    for indicator in suspicious_indicators:
        if indicator in normalized_command:
            # 🛡️ إجراء حماية ذكي: حظر الطلب وتوثيق الهجوم فوراً
            print(f"\n[RASP ENGAGED] Critical Threat Intercepted: Execution of '{command}' blocked!")
            print("[RASP ACTION] Request Blocked successfully. Server remains online.")
            return False # إرجاع خطأ لإحباط العملية فقط
            
    return True

@app.route('/api/v1/execute', methods=['POST'])
def vulnerable_endpoint():
    """نقطة نهاية تحاكي ثغرة للتنفيذ لكنها محمية بالـ RASP"""
    data = request.get_json() or {}
    user_input = data.get("cmd", "")
    
    if not user_input:
        return jsonify({"status": "Error", "output": "No command provided"}), 400
        
    print(f"[Runtime Log] Received command execution request: {user_input}")
    
    # 🛡️ استدعاء الـ RASP للحماية الذاتية
    if not rasp_runtime_monitor(user_input):
        return jsonify({
            "status": "Blocked", 
            "reason": "RASP Self-Protection Triggered. Malicious command blocked."
        }), 403
        
    # تنفيذ الأمر بأمان في حال تخطي الفحص الطبيعي
    try:
        result = subprocess.check_output(user_input, shell=True, stderr=subprocess.STDOUT, text=True)
        return jsonify({"status": "Success", "output": result})
    except Exception as e:
        return jsonify({"status": "Error", "output": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Vulnerable Web App running with Active RASP Monitor on port 8080...")
    app.run(host='0.0.0.0', port=8080)
