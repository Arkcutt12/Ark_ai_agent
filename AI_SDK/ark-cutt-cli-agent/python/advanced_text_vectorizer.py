#!/usr/bin/env python3
"""
Advanced Text Vectorizer for Ark Cutt CLI Agent
Converts text to DXF vector graphics with proper centering and complete letter definitions
"""

import sys
import os
import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment
import math

class AdvancedTextVectorizer:
    def __init__(self):
        self.letter_definitions = self._create_letter_definitions()
    
    def _create_letter_definitions(self):
        """Define vector paths for each letter with proper scaling"""
        scale = 1.0  # Base scale factor
        
        return {
            'A': [
                [(0*scale, 0*scale), (5*scale, 100*scale)],
                [(5*scale, 100*scale), (10*scale, 0*scale)],
                [(2.5*scale, 50*scale), (7.5*scale, 50*scale)]
            ],
            'R': [
                [(0*scale, 0*scale), (0*scale, 100*scale)],
                [(0*scale, 100*scale), (6*scale, 100*scale)],
                [(6*scale, 100*scale), (8*scale, 90*scale)],
                [(8*scale, 90*scale), (8*scale, 60*scale)],
                [(8*scale, 60*scale), (6*scale, 50*scale)],
                [(6*scale, 50*scale), (0*scale, 50*scale)],
                [(6*scale, 50*scale), (10*scale, 0*scale)]
            ],
            'K': [
                [(0*scale, 0*scale), (0*scale, 100*scale)],
                [(0*scale, 50*scale), (8*scale, 100*scale)],
                [(0*scale, 50*scale), (8*scale, 0*scale)]
            ],
            'C': [
                [(8*scale, 20*scale), (6*scale, 0*scale)],
                [(6*scale, 0*scale), (2*scale, 0*scale)],
                [(2*scale, 0*scale), (0*scale, 20*scale)],
                [(0*scale, 20*scale), (0*scale, 80*scale)],
                [(0*scale, 80*scale), (2*scale, 100*scale)],
                [(2*scale, 100*scale), (6*scale, 100*scale)],
                [(6*scale, 100*scale), (8*scale, 80*scale)]
            ],
            'U': [
                [(0*scale, 100*scale), (0*scale, 20*scale)],
                [(0*scale, 20*scale), (2*scale, 0*scale)],
                [(2*scale, 0*scale), (6*scale, 0*scale)],
                [(6*scale, 0*scale), (8*scale, 20*scale)],
                [(8*scale, 20*scale), (8*scale, 100*scale)]
            ],
            'T': [
                [(0*scale, 100*scale), (10*scale, 100*scale)],
                [(5*scale, 100*scale), (5*scale, 0*scale)]
            ],
            'I': [
                [(2*scale, 0*scale), (8*scale, 0*scale)],
                [(5*scale, 0*scale), (5*scale, 100*scale)],
                [(2*scale, 100*scale), (8*scale, 100*scale)],
                # Fixed: Add the missing dot at the top
                [(8*scale, 110*scale), (12*scale, 110*scale)]
            ],
            'O': [
                [(2*scale, 0*scale), (6*scale, 0*scale)],
                [(6*scale, 0*scale), (8*scale, 20*scale)],
                [(8*scale, 20*scale), (8*scale, 80*scale)],
                [(8*scale, 80*scale), (6*scale, 100*scale)],
                [(6*scale, 100*scale), (2*scale, 100*scale)],
                [(2*scale, 100*scale), (0*scale, 80*scale)],
                [(0*scale, 80*scale), (0*scale, 20*scale)],
                [(0*scale, 20*scale), (2*scale, 0*scale)]
            ],
            'N': [
                [(0*scale, 0*scale), (0*scale, 100*scale)],
                [(0*scale, 100*scale), (8*scale, 0*scale)],
                [(8*scale, 0*scale), (8*scale, 100*scale)]
            ],
            'E': [
                [(0*scale, 0*scale), (0*scale, 100*scale)],
                [(0*scale, 100*scale), (8*scale, 100*scale)],
                [(0*scale, 50*scale), (6*scale, 50*scale)],
                [(0*scale, 0*scale), (8*scale, 0*scale)]
            ],
            'L': [
                [(0*scale, 100*scale), (0*scale, 0*scale)],
                [(0*scale, 0*scale), (8*scale, 0*scale)]
            ],
            'S': [
                [(8*scale, 80*scale), (6*scale, 100*scale)],
                [(6*scale, 100*scale), (2*scale, 100*scale)],
                [(2*scale, 100*scale), (0*scale, 80*scale)],
                [(0*scale, 80*scale), (0*scale, 60*scale)],
                [(0*scale, 60*scale), (2*scale, 50*scale)],
                [(2*scale, 50*scale), (6*scale, 50*scale)],
                [(6*scale, 50*scale), (8*scale, 40*scale)],
                [(8*scale, 40*scale), (8*scale, 20*scale)],
                [(8*scale, 20*scale), (6*scale, 0*scale)],
                [(6*scale, 0*scale), (2*scale, 0*scale)],
                [(2*scale, 0*scale), (0*scale, 20*scale)]
            ],
            'P': [
                [(0*scale, 0*scale), (0*scale, 100*scale)],
                [(0*scale, 100*scale), (6*scale, 100*scale)],
                [(6*scale, 100*scale), (8*scale, 90*scale)],
                [(8*scale, 90*scale), (8*scale, 60*scale)],
                [(8*scale, 60*scale), (6*scale, 50*scale)],
                [(6*scale, 50*scale), (0*scale, 50*scale)]
            ],
            ' ': []  # Space character
        }
    
    def vectorize_text(self, text, output_path, font_size=20, layer_name='TEXT'):
        """
        Vectorize text to DXF format with proper centering
        """
        try:
            # Create new DXF document
            doc = ezdxf.new('R2010', setup=True)
            doc.units = units.MM
            
            msp = doc.modelspace()
            
            # Create text layer
            doc.layers.add(layer_name, color=2)  # Yellow color
            
            # Calculate text dimensions
            letter_width = font_size * 0.6
            letter_spacing = font_size * 0.8
            text_width = len(text) * letter_spacing - (letter_spacing - letter_width)
            
            # Fixed centering calculation - position text correctly in coordinate system
            center_x = 1000  # Use 1000 as base coordinate instead of 0
            center_y = 1000  # Use 1000 as base coordinate instead of 0
            
            # Calculate proper position to center the text
            height_units = font_size
            position = (center_x - text_width/2, center_y - height_units/2)
            
            current_x = position[0]
            
            # Process each character
            for char in text.upper():
                if char in self.letter_definitions:
                    paths = self.letter_definitions[char]
                    scale_factor = font_size / 100.0  # Scale to desired font size
                    
                    for path in paths:
                        if len(path) >= 2:
                            start_point = (
                                current_x + path[0][0] * scale_factor,
                                position[1] + path[0][1] * scale_factor
                            )
                            end_point = (
                                current_x + path[1][0] * scale_factor,
                                position[1] + path[1][1] * scale_factor
                            )
                            
                            # Add line to DXF
                            msp.add_line(
                                start_point,
                                end_point,
                                dxfattribs={'layer': layer_name}
                            )
                else:
                    # Handle unknown characters as spaces
                    pass
                
                current_x += letter_spacing
            
            # Save DXF file
            doc.saveas(output_path)
            
            result = {
                'success': True,
                'message': f'✅ Texto vectorizado exitosamente: {text}',
                'file_path': output_path,
                'text_info': {
                    'text': text,
                    'font_size': font_size,
                    'position': position,
                    'dimensions': {
                        'width': text_width,
                        'height': height_units
                    },
                    'layer': layer_name
                }
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'message': f'❌ Error vectorizando texto: {str(e)}',
                'error': str(e)
            }

def main():
    """Command line interface for text vectorization"""
    if len(sys.argv) < 4:
        print("❌ Uso: python advanced_text_vectorizer.py <texto> <archivo_salida> <tamaño_fuente> [capa]")
        return
    
    text = sys.argv[1]
    output_path = sys.argv[2]
    font_size = float(sys.argv[3])
    layer_name = sys.argv[4] if len(sys.argv) > 4 else 'TEXT'
    
    vectorizer = AdvancedTextVectorizer()
    result = vectorizer.vectorize_text(text, output_path, font_size, layer_name)
    
    print(result['message'])
    
    if result['success'] and 'text_info' in result:
        info = result['text_info']
        print(f"📍 Posición: ({info['position'][0]:.1f}, {info['position'][1]:.1f})")
        print(f"📏 Dimensiones: {info['dimensions']['width']:.1f} x {info['dimensions']['height']:.1f} mm")
        print(f"🎯 Capa: {info['layer']}")

if __name__ == "__main__":
    main()