import streamlit as st


def render_help():
    st.header("❓ Guía de Lectura")
    st.write(
        """
        Algunas gráficas de este *dashboard* usan técnicas estadísticas que no son evidentes
        a simple vista. Aquí se explican los términos y conceptos más técnicos, organizados
        por la pestaña donde aparecen.
        """
    )

    st.divider()
    st.subheader("📖 Términos generales")

    with st.expander("¿Qué es un \"ingreso\"? ¿Por qué no se habla de \"pacientes\"?"):
        st.write(
            """
            La unidad de análisis de este *dashboard* es el **ingreso en UCI**, no la persona. 
            Un mismo paciente puede tener más de un ingreso, así que cuando se ve "1.234 ingresos" no
            significa necesariamente 1.234 personas distintas.
            """
        )

    with st.expander("¿Qué significa \"conjunto de test\"?"):
        st.write(
            """
            Los tres modelos se entrenaron con un 80% de los datos (conjunto de
            entrenamiento) y se evaluaron con el 20% restante que el modelo nunca vio
            durante el entrenamiento (conjunto de test). Las gráficas de rendimiento en las
            pestañas de Mortalidad y Estancia muestran resultados sobre ese 20%, es la
            única forma honesta de medir cómo se comporta el modelo con datos nuevos.
            """
        )

    with st.expander("¿Qué son los \"puntos porcentuales (p.p.)\"?"):
        st.write(
            """
            Es la resta directa entre dos porcentajes, no una comparación relativa. Si la
            mortalidad global es 12% y un grupo tiene 19%, la diferencia es **+7 p.p.**.
            """
        )

    st.divider()
    st.subheader("🎯 Clasificación de Mortalidad")

    with st.expander("¿Qué es la matriz de confusión?"):
        st.write(
            """
            Compara las predicciones del modelo con los eventos reales mediante una tabla 2x2.
            Se analiza el rendimiento del algoritmo diferenciando los aciertos (pacientes cuya 
            supervivencia o fallecimiento se predijo correctamente) de los errores de clasificación 
            (falsos positivos y falsos negativos). La diagonal principal agrupa todas las 
            predicciones correctas.
            """
        )

    with st.expander("¿Qué diferencia hay entre el umbral \"por defecto\" y el \"ajustado\"?"):
        st.write(
            """
            El modelo no predice directamente "vive/muere", sino una probabilidad (0 a 1).
            El umbral decide a partir de qué probabilidad se clasifica como "alto riesgo".
            El umbral **por defecto (0.5)** es el estándar, el **ajustado (óptimo F1)** se
            calculó para equilibrar mejor precisión y sensibilidad, dado que la mortalidad
            es un evento minoritario (hay muchos más supervivientes que fallecidos).
            """
        )

    with st.expander("¿Qué es SHAP y cómo se lee el gráfico de impacto (beeswarm)?"):
        st.write(
            """
            SHAP mide cuánto empuja cada variable la predicción de un ingreso concreto,
            hacia arriba (más riesgo) o hacia abajo (menos riesgo), respecto a la
            predicción media. En el gráfico de puntos ("beeswarm"), el eje X es ese
            impacto (valor SHAP), y el color representa si el valor de esa variable en ese
            ingreso era bajo (azul) o alto (magenta/rojo). Por ejemplo, si `Age` tiene
            puntos rojos a la derecha, significa que las edades altas empujan el riesgo
            hacia arriba.
            """
        )

    with st.expander("¿Por qué se comparan APS y APACHE Score con el riesgo predicho?"):
        st.write(
            """
            APS y APACHE Score son escalas de gravedad clínica ya validadas y usadas en la
            práctica real. Comparar el riesgo que predice el modelo con estas escalas es
            una forma de comprobar si el modelo "entiende" la gravedad de forma parecida a
            como lo hace la medicina establecida, no solo si acierta en los datos de
            entrenamiento.
            """
        )

    with st.expander("¿Qué es la correlación de Spearman?"):
        st.write(
            """
            Mide si dos variables suben y bajan juntas en el mismo orden, sin asumir que la
            relación sea una línea recta (a diferencia de la correlación de Pearson). Va de
            -1 a 1, cerca de 1 significa que a más gravedad clínica, más riesgo predice el
            modelo, de forma consistente.
            """
        )

    st.divider()
    st.subheader("🏨 Regresión de Estancia")

    with st.expander("¿Por qué el eje de días está en escala logarítmica?"):
        st.write(
            """
            La duración de la estancia en UCI es muy asimétrica, la mayoría de ingresos
            duran pocos días, pero unos pocos duran semanas o meses. En una escala lineal
            normal, esos casos largos "aplastarían" visualmente a la mayoría de los datos
            contra el cero. La escala logarítmica reparte mejor el espacio sin ocultar los 
            eventos de larga duración. Las etiquetas del eje siguen mostrando días reales 
            en lugar de logaritmos.
            """
        )

    with st.expander("¿Qué diferencia hay entre MAE y RMSE?"):
        st.write(
            """
            Ambos miden el error medio del modelo en días. El **MAE** (error absoluto
            medio) trata todos los errores por igual y el **RMSE** (raíz del error
            cuadrático medio) penaliza más los errores grandes. Si el RMSE es mucho mayor
            que el MAE, significa que el modelo comete algunos errores muy grandes en
            ciertos casos, aunque en promedio acierte razonablemente bien.
            """
        )

    with st.expander("¿Qué son los residuos?"):
        st.write(
            """
            Los residuos son la diferencia entre la estancia real y la que predijo el modelo
            (`real - predicho`) para cada ingreso. Un residuo positivo significa que el
            ingreso duró más de lo que el modelo predijo y un residuo negativo significa 
            que la estancia duró menos que lo predicho.
            """
        )

    with st.expander("¿Qué es la importancia de variables (feature importance)?"):
        st.write(
            """
            Un ranking de qué variables usa más el modelo para hacer sus predicciones, en
            conjunto (no ingreso a ingreso a diferencia de SHAP). Es una propiedad fija
            del modelo ya entrenado, así que los filtros de la sidebar no la modifican.
            """
        )

    st.divider()
    st.subheader("📊 Clustering de Fenotipos")

    with st.expander("¿Qué diferencia hay entre K-Means y GMM?"):
        st.write(
            """
            Son dos algoritmos distintos para agrupar ingresos en clústeres sin usar la
            variable de mortalidad. **K-Means** asigna cada ingreso a un único grupo según
            la distancia a un centro. **GMM** (Gaussian Mixture Model) es más flexible,
            modela cada grupo como una distribución estadística, lo que permite formas de
            clúster menos rígidas. Pueden dar un número distinto de grupos y agrupaciones
            algo diferentes, por eso el *dashboard* permite elegir qué algoritmo ver.
            """
        )

    with st.expander("¿Cómo leer el radar de constantes vitales?"):
        st.write(
            """
            Compara la mediana de un clúster con la mediana global en varias variables a
            la vez (frecuencia cardíaca, edad, temperatura...). Como cada variable tiene
            unidades distintas, los ejes están normalizados (0 a 1) para que se muestre en el
            mismo gráfico. Los valores reales con sus unidades están en la tabla justo
            debajo del radar.
            """
        )

    with st.expander("¿Por qué el PCA solo explica una parte pequeña de la varianza?"):
        st.write(
            """
            El PCA reduce decenas de variables clínicas a solo 2 dimensiones (PC1 y PC2)
            para poder dibujarlas en un plano. Con datos clínicos complejos, esas 2
            dimensiones no siempre capturan toda la información. El gráfico es útil como
            mapa exploratorio para ver si los clústeres se separan visualmente, pero no
            como prueba definitiva de que los grupos son distintos entre sí.
            """
        )