import React, { useState, useEffect } from 'react';
import { Button, Form, Table, Alert } from 'react-bootstrap';

export const Tarea = () => {
  const [tareas, setTareas] = useState([]);
  const [titulo, setTitulo] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [estado, setEstado] = useState(false); 
  const [editando, setEditando] = useState(false);
  const [idEditando, setIdEditando] = useState(null);
  const [error, setError] = useState('');

  const endpoint = 'http://localhost:8000/task'; 
  useEffect(() => {
    const obtenerTareas = async () => {
      try {
        const response = await fetch(endpoint);
        const data = await response.json();
        setTareas(data);
      } catch (error) {
        console.error('Error al obtener tareas:', error);
        setError('Error al obtener las tareas');
      }
    };
    obtenerTareas();
  }, []);

  const agregarTarea = async () => {
    if (titulo && descripcion) {
      const nuevaTarea = { titulo, descripcion, estado };

      try {
        const response = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(nuevaTarea),
        });
        const data = await response.json();
        setTareas([...tareas, data]); // Actualizar estado con la nueva tarea
        resetFormulario();
      } catch (error) {
        console.error('Error al agregar tarea:', error);
        setError('Error al agregar la tarea');
      }
    } else {
      setError('Debe llenar todos los campos');
    }
  };

  // Eliminar tarea
  const eliminarTarea = async (id) => {
    try {
      await fetch(`${endpoint}/${id}`, { method: 'DELETE' });
      const nuevasTareas = tareas.filter((tarea) => tarea.id !== id);
      setTareas(nuevasTareas);
    } catch (error) {
      console.error('Error al eliminar tarea:', error);
      setError('Error al eliminar la tarea');
    }
  };

  const editarTarea = (tarea) => {
    setEditando(true);
    setTitulo(tarea.titulo);
    setDescripcion(tarea.descripcion);
    setEstado(tarea.estado);
    setIdEditando(tarea.id);
  };

  const actualizarTarea = async () => {
    const tareaActualizada = { titulo, descripcion, estado };
    try {
      const response = await fetch(`${endpoint}/${idEditando}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(tareaActualizada),
      });
      const data = await response.json();
      const nuevasTareas = tareas.map((tarea) =>
        tarea.id === idEditando ? data : tarea
      );
      setTareas(nuevasTareas); 
      resetFormulario();
    } catch (error) {
      console.error('Error al actualizar tarea:', error);
      setError('Error al actualizar la tarea');
    }
  };

  // Limpiar formulario
  const resetFormulario = () => {
    setTitulo('');
    setDescripcion('');
    setEstado(false);
    setEditando(false);
    setIdEditando(null);
    setError('');
  };

  return (
    <div className="container">
      <h2 className="mt-4">Gestión de Tareas</h2>

      {error && <Alert variant="danger">{error}</Alert>}

      <Form className="mt-4">
        <Form.Group className="mb-3">
          <Form.Label>Título</Form.Label>
          <Form.Control
            type="text"
            placeholder="Ingrese el título"
            value={titulo}
            onChange={(e) => setTitulo(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Descripción</Form.Label>
          <Form.Control
            as="textarea"
            rows={3}
            placeholder="Ingrese la descripción"
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Estado</Form.Label>
          <Form.Select value={estado} onChange={(e) => setEstado(e.target.value === 'true')}>
            <option value="false">Pendiente</option>
            <option value="true">Completada</option>
          </Form.Select>
        </Form.Group>

        <Button
          variant={editando ? 'warning' : 'primary'}
          onClick={editando ? actualizarTarea : agregarTarea}
        >
          {editando ? 'Actualizar Tarea' : 'Añadir Tarea'}
        </Button>
      </Form>

      <Table className="mt-4">
        <thead>
          <tr>
            <th>#</th>
            <th>Título</th>
            <th>Descripción</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {tareas.map((tarea, index) => (
            <tr key={tarea.id}>
              <td>{index + 1}</td>
              <td>{tarea.titulo}</td>
              <td>{tarea.descripcion}</td>
              <td>{tarea.estado ? 'Completada' : 'Pendiente'}</td>
              <td>
                <Button
                  variant="warning"
                  className="me-2"
                  onClick={() => editarTarea(tarea)}
                >
                  Editar
                </Button>
                <Button variant="danger" onClick={() => eliminarTarea(tarea.id)}>
                  Eliminar
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};
