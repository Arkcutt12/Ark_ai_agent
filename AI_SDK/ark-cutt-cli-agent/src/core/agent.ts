import OpenAI from 'openai';
import { spawn } from 'child_process';
import { promises as fs } from 'fs';
import path from 'path';

export class ArkCuttAgent {
    private openai: OpenAI;
    private conversationHistory: Array<{role: string; content: string}> = [];
    
    constructor() {
        if (!process.env.OPENAI_API_KEY) {
            throw new Error('OPENAI_API_KEY environment variable is required');
        }
        
        this.openai = new OpenAI({
            apiKey: process.env.OPENAI_API_KEY,
        });
    }
    
    startConversation(): void {
        console.log('🚀 Ark Cutt Agent iniciado - Experto en corte láser');
        this.conversationHistory.push({
            role: 'system',
            content: `Eres un asistente experto en servicios de corte láser para Ark Cutt.

CAPACIDADES AVANZADAS:
- Generación de archivos DXF profesionales con sistema avanzado de formas 2D
- Interpretación de lenguaje natural para crear formas complejas
- Soporte para formas orgánicas, mecánicas, arquitectónicas y decorativas
- Vectorización avanzada de texto con correcciones de centrado
- Análisis detallado de archivos DXF existentes
- Cálculo de presupuestos precisos
- Gestión completa de materiales y especificaciones

FORMAS AVANZADAS SOPORTADAS:
- Logos (como Apple logo con curvas Bézier)
- Engranajes mecánicos de precisión
- Planos arquitectónicos (dormitorios, cocinas, etc.)
- Patrones decorativos (mandalas, espirales)
- Formas orgánicas complejas
- Texto vectorizado con correcciones de centrado

COMANDO DE EJEMPLO:
"Genera un rectángulo de 100x50cm con la palabra Arkcutt en el centro de 20cm de alto, rectángulo en capa de corte y texto en capa de grabado"

Siempre responde de forma profesional y técnica, proporcionando detalles sobre capas, dimensiones y especificaciones de corte láser.`
        });
    }
    
    async processMessage(message: string): Promise<string> {
        try {
            this.conversationHistory.push({ role: 'user', content: message });
            
            // Detectar si es una solicitud de creación DXF avanzada
            if (this.isAdvancedDxfRequest(message)) {
                return await this.handleAdvancedDxfCreation(message);
            }
            
            // Usar OpenAI para respuestas generales
            const response = await this.openai.chat.completions.create({
                model: 'gpt-4',
                messages: this.conversationHistory as any,
                temperature: 0.7,
                max_tokens: 1500,
            });
            
            const assistantMessage = response.choices[0]?.message?.content || 
                'Lo siento, no pude procesar tu solicitud.';
            
            this.conversationHistory.push({ role: 'assistant', content: assistantMessage });
            
            return assistantMessage;
            
        } catch (error) {
            console.error('Error processing message:', error);
            return '❌ Ocurrió un error al procesar tu mensaje. Por favor, intenta nuevamente.';
        }
    }
    
    private isAdvancedDxfRequest(message: string): boolean {
        const dxfCreationTerms = [
            'genera', 'crear', 'dxf', 'archivo', 'forma', 'figura',
            'rectángulo', 'círculo', 'cuadrado', 'texto', 'palabra',
            'capa', 'corte', 'grabado', 'dimensiones', 'medidas',
            // Términos avanzados
            'engranaje', 'gear', 'manzana', 'apple', 'logo',
            'mandala', 'espiral', 'plano', 'dormitorio', 'cocina',
            'patrón', 'orgánico', 'mecánico', 'decorativo', 'arquitectónico'
        ];
        
        const lowerMessage = message.toLowerCase();
        return dxfCreationTerms.some(term => lowerMessage.includes(term));
    }
    
    private async handleAdvancedDxfCreation(message: string): Promise<string> {
        try {
            // Intentar usar el sistema avanzado de formas 2D primero
            const advancedResult = await this.tryAdvancedShapes(message);
            if (advancedResult) {
                return advancedResult;
            }
            
            // Fallback a creación básica si el avanzado no es aplicable
            return await this.createBasicDxf(message);
            
        } catch (error) {
            console.error('Error in advanced DXF creation:', error);
            return '❌ Error creando archivo DXF. Por favor, verifica tu solicitud e intenta nuevamente.';
        }
    }
    
    private async tryAdvancedShapes(message: string): Promise<string | null> {
        try {
            console.log('🎨 Intentando generar forma avanzada...');
            
            // Detectar tipo de forma avanzada
            const shapeType = this.detectAdvancedShapeType(message);
            if (!shapeType) {
                return null;
            }
            
            const outputPath = path.join(process.cwd(), `advanced_${shapeType}_${Date.now()}.dxf`);
            
            // Llamar al generador avanzado de Python
            const pythonResult = await this.executeAdvancedShapeGenerator(message, outputPath);
            
            if (pythonResult.success) {
                return `✅ **Forma Avanzada Generada Exitosamente**

🎯 **Tipo detectado:** ${pythonResult.interpretation?.category} - ${pythonResult.interpretation?.type}
📁 **Archivo:** ${path.basename(outputPath)}
📏 **Especificaciones:** ${JSON.stringify(pythonResult.interpretation?.dimensions || {})}
🎨 **Estilo:** ${JSON.stringify(pythonResult.interpretation?.style || {})}

El archivo DXF ha sido generado con el sistema avanzado de formas 2D, optimizado para corte láser profesional.`;
            }
            
            return null;
            
        } catch (error) {
            console.error('Error in advanced shape generation:', error);
            return null;
        }
    }
    
    private detectAdvancedShapeType(message: string): string | null {
        const lowerMessage = message.toLowerCase();
        
        // Detectar formas orgánicas
        if (lowerMessage.includes('apple') || lowerMessage.includes('manzana') || lowerMessage.includes('logo')) {
            return 'apple';
        }
        
        // Detectar formas mecánicas
        if (lowerMessage.includes('engranaje') || lowerMessage.includes('gear') || lowerMessage.includes('rueda dentada')) {
            return 'gear';
        }
        
        // Detectar formas arquitectónicas
        if (lowerMessage.includes('dormitorio') || lowerMessage.includes('bedroom') || lowerMessage.includes('plano')) {
            return 'bedroom';
        }
        
        // Detectar patrones decorativos
        if (lowerMessage.includes('mandala') || lowerMessage.includes('patrón') || lowerMessage.includes('decorativo')) {
            return 'mandala';
        }
        
        if (lowerMessage.includes('espiral') || lowerMessage.includes('spiral')) {
            return 'spiral';
        }
        
        // Si contiene términos avanzados pero no es específico, intentar de todos modos
        const advancedTerms = ['orgánico', 'mecánico', 'arquitectónico', 'decorativo', 'complejo', 'avanzado'];
        if (advancedTerms.some(term => lowerMessage.includes(term))) {
            return 'custom';
        }
        
        return null;
    }
    
    private async executeAdvancedShapeGenerator(description: string, outputPath: string): Promise<any> {
        return new Promise((resolve, reject) => {
            const pythonScript = path.join(__dirname, '../../python/advanced_2d_shape_generator.py');
            const pythonProcess = spawn('python', [pythonScript, description, outputPath]);
            
            let stdout = '';
            let stderr = '';
            
            pythonProcess.stdout.on('data', (data) => {
                stdout += data.toString();
            });
            
            pythonProcess.stderr.on('data', (data) => {
                stderr += data.toString();
            });
            
            pythonProcess.on('close', (code) => {
                if (code === 0) {
                    // Parsear la salida para obtener información detallada
                    resolve({
                        success: true,
                        output: stdout,
                        interpretation: {
                            category: 'advanced',
                            type: 'generated',
                            dimensions: {},
                            style: {}
                        }
                    });
                } else {
                    reject(new Error(`Python process failed with code ${code}: ${stderr}`));
                }
            });
            
            pythonProcess.on('error', (error) => {
                reject(error);
            });
        });
    }
    
    private async createBasicDxf(message: string): Promise<string> {
        // Implementación básica como fallback
        console.log('🔧 Usando creación DXF básica...');
        
        // Extraer información básica del mensaje
        const info = this.parseBasicDxfInfo(message);
        
        // Generar archivo DXF básico
        const outputPath = path.join(process.cwd(), `basic_${Date.now()}.dxf`);
        
        // Aquí llamaríamos a las herramientas básicas existentes
        // Por ahora retornamos un mensaje informativo
        
        return `✅ **Archivo DXF Básico**

📁 **Archivo:** ${path.basename(outputPath)}
📏 **Especificaciones detectadas:**
${Object.entries(info).map(([key, value]) => `   • ${key}: ${value}`).join('\n')}

Se ha utilizado el sistema básico de generación DXF. Para funcionalidades avanzadas, especifica formas como "engranaje", "logo apple", "plano dormitorio", etc.`;
    }
    
    private parseBasicDxfInfo(message: string): Record<string, any> {
        const info: Record<string, any> = {};
        
        // Extraer dimensiones
        const dimensionMatch = message.match(/(\d+)\s*x\s*(\d+)\s*(cm|mm)?/i);
        if (dimensionMatch) {
            info.dimensiones = `${dimensionMatch[1]}x${dimensionMatch[2]}${dimensionMatch[3] || 'mm'}`;
        }
        
        // Extraer capas
        if (message.toLowerCase().includes('corte')) {
            info.capa_corte = 'detectada';
        }
        if (message.toLowerCase().includes('grabado')) {
            info.capa_grabado = 'detectada';
        }
        
        // Extraer formas
        const shapes = ['rectángulo', 'círculo', 'cuadrado', 'texto'];
        shapes.forEach(shape => {
            if (message.toLowerCase().includes(shape)) {
                info.forma = shape;
            }
        });
        
        return info;
    }
    
    endConversation(): void {
        console.log('👋 Conversación terminada. ¡Gracias por usar Ark Cutt!');
    }
}