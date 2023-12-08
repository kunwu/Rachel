declare module "*.vue" {
    import { defineComponent } from 'vue';
    const compnent: ReturnType<typeof defineComponent>;
    export default compnent;
  }
  