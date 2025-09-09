#!/usr/bin/env node

// Test completo end-to-end: DXF analysis + Budget calculation
// Configurar dotenv para cargar variables de entorno
require('dotenv').config();

const { BudgetTool } = require('./dist/tools/budget-tool');

async function testFullFlow() {
  console.log('🧪 Probando flujo completo end-to-end...\n');
  console.log('📋 DXF Analysis + Budget Calculation\n');
  
  const budgetTool = new BudgetTool();
  
  try {
    console.log('🚀 Iniciando generación de presupuesto completo...');
    
    const result = await budgetTool.generateBudget({
      dxfFilePath: 'C:\\Users\\hiero\\Desktop\\ARCHIVOS_DXF_GOOD\\Jan-Diaz_Fachada.dxf',
      material: 'Metacrilato',
      color: 'transparente',
      thickness: 3,
      urgency: 'standard',
      clientInfo: {
        name: 'Juan Pérez Test',
        email: 'juan.test@example.com',
        phone: '+34 600 123 456'
      }
    });
    
    console.log('\n✅ ¡ÉXITO! Flujo completo funcionando');
    console.log('📄 Resultado del presupuesto:');
    console.log(result);
    
  } catch (error) {
    console.log('\n❌ Error en el flujo completo:', error.message);
    
    // Diagnosticar el tipo de error
    if (error.message.includes('Request failed with status code')) {
      const statusMatch = error.message.match(/status code (\d+)/);
      if (statusMatch) {
        const status = statusMatch[1];
        console.log(`\n🔍 Diagnóstico - Error HTTP ${status}:`);
        
        switch (status) {
          case '404':
            console.log('- El endpoint no existe o la URL es incorrecta');
            break;
          case '422':
            console.log('- Datos de entrada inválidos o campos faltantes');
            break;
          case '500':
            console.log('- Error interno del servidor');
            break;
          default:
            console.log('- Error desconocido del servidor');
        }
      }
    }
  }
}

testFullFlow().catch(console.error);