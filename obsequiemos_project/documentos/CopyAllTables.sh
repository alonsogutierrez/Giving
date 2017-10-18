#!/bin/bash

#Script para rellenar la base de datos con la data parámetrica

psql -U alonso -d testgiving  << EOF

\copy obsequiemos_usertype from 'tipos_usuario.txt' (delimiter(','))

\copy obsequiemos_categorygift from 'categoria_gift.txt' (delimiter(','));

\copy obsequiemos_subcategorygift from 'subcategoria_gift.txt' (delimiter(','));

\copy obsequiemos_giftweighttype from 'tipo_peso_gift.txt' (delimiter(','));

\copy obsequiemos_usedtimetype from 'tiempo_uso_gift.txt' (delimiter(','));

\copy obsequiemos_giftdimensiontype from 'tipo_dimension_gift.txt' (delimiter(','));

\copy obsequiemos_giftstatetype from 'tipo_estado_gift.txt' (delimiter(','));

\copy obsequiemos_poststatetype from 'tipo_estado_post.txt' (delimiter(','));

\copy obsequiemos_dispatchmethod from 'tipo_metodo_despacho.txt' (delimiter(','));

\copy obsequiemos_regionpost from 'regiones.txt' (delimiter(','));

\copy obsequiemos_provinciapost from 'provincias.txt' (delimiter(','));

\copy obsequiemos_comunapost from 'comunas.txt' (delimiter(','));

EOF





